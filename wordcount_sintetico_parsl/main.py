import argparse
import sys
import time
from pathlib import Path

import networkx as nx
import parsl

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps import (
    merge_outputs_synthetic,
    reduce_bucket_synthetic,
    wordcount_bucketed_synthetic,
)
from config import gen_config

from workflowbuilder import *


def build_synthetic_workflow(num_files, num_buckets, wordcount_time, reduce_time, merge_time):
    wf = Workflow()

    maps = []
    for i in range(num_files):
        name = f"wordcount_bucketed_{i}"
        wf.add_pattern(SingleTask(name, wordcount_time))
        maps.append(name)

    final_buckets = []
    for b in range(num_buckets):
        current_level = maps.copy()
        round_id = 1

        while len(current_level) > 1:
            next_level = []

            for i in range(0, len(current_level), 2):
                left = current_level[i]

                if i + 1 >= len(current_level):
                    next_level.append(left)
                    continue

                right = current_level[i + 1]
                reduce_name = f"reduce_bucket_b{b}_r{round_id}_{i//2}"

                wf.add_pattern(SingleTask(reduce_name, reduce_time))
                wf.add_pattern_edge(left, reduce_name)
                wf.add_pattern_edge(right, reduce_name)

                next_level.append(reduce_name)

            current_level = next_level
            round_id += 1

        final_buckets.append(current_level[0])

    wf.add_pattern(SingleTask("merge_outputs", merge_time))
    for bucket_final in final_buckets:
        wf.add_pattern_edge(bucket_final, "merge_outputs")

    wf.set_new_root("wordcount_bucketed_0")
    wf.parse(time_as_arg=True)

    return wf


def submit_node(node, duration, inputs, work_mode):
    if node.startswith("wordcount_bucketed_"):
        return wordcount_bucketed_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("reduce_bucket_"):
        return reduce_bucket_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("merge_outputs_"):
        return merge_outputs_synthetic(node, duration, work_mode, inputs=inputs)

    raise ValueError(f"Unknown synthetic task type for node: {node}")


def run_parsl_from_workflow(wf, work_mode):
    futures = {}

    for node in nx.topological_sort(wf.dag_parsed):
        parents = list(wf.dag_parsed.predecessors(node))
        inputs = [futures[parent] for parent in parents]
        duration = wf.dag_parsed.nodes[node].get("time", 1)
        futures[node] = submit_node(node, duration, inputs, work_mode)

    sink_nodes = [node for node in wf.dag_parsed.nodes if wf.dag_parsed.out_degree(node) == 0]
    return [futures[node].result() for node in sink_nodes]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", type=int, default=100)
    parser.add_argument("--buckets", type=int, default=48)
    parser.add_argument("--wordcount-time", type=float, default=206.95)
    parser.add_argument("--reduce-time", type=float, default=15.29)
    parser.add_argument("--merge-time", type=float, default=886.03)
    parser.add_argument("--time-scale", type=float, default=1.0)
    parser.add_argument("--work-mode", choices=["sleep", "cpu"], default="sleep")
    parser.add_argument("--export-pdf", action="store_true")
    parser.add_argument("--onslurm", action="store_true")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--monitor", action="store_true")
    
    args = parser.parse_args()

    cfg = gen_config(
        threads=args.threads,
        monitoring=args.monitor,
        slurm=args.onslurm,
    )
    parsl.load(cfg)

    wordcount_time = args.wordcount_time * args.time_scale
    reduce_time = args.reduce_time * args.time_scale
    merge_time = args.merge_time * args.time_scale

    print(f"[INFO] files={args.files}")
    print(f"[INFO] buckets={args.buckets}")
    print(f"[INFO] wordcount_time={wordcount_time}")
    print(f"[INFO] reduce_time={reduce_time}")
    print(f"[INFO] merge_time={merge_time}")
    print(f"[INFO] time_scale={args.time_scale}")
    print(f"[INFO] work_mode={args.work_mode}")
    print(f"[INFO] slurm={args.onslurm}")

    start = time.time()

    try:
        workflow = build_synthetic_workflow(
            args.files,
            args.buckets,
            wordcount_time,
            reduce_time,
            merge_time,
        )
        if args.export_pdf:
            workflow.export_pydot(filename="wordcount_sintetico_workflowbuilder.pdf")

        results = run_parsl_from_workflow(workflow, args.work_mode)
        elapsed = time.time() - start

        print("\n[OK] Workflow sintetico finalizado.")
        print(f"[OK] Resultado final: {results}")
        print(f"[OK] Makespan observado: {elapsed:.2f} s")
        print(f"[OK] Total nodes: {workflow.dag_parsed.number_of_nodes()}")
        print(f"[OK] Total edges: {workflow.dag_parsed.number_of_edges()}")
        print(f"[OK] WordCount tasks: {args.files}")
        print(f"[OK] Reduce tasks: {args.buckets * (args.files - 1)}")
        print("[OK] Merge tasks: 1")
    finally:
        parsl.dfk().cleanup()
        parsl.clear()
