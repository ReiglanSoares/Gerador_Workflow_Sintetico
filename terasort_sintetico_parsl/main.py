import argparse
import sys
import time
from pathlib import Path

import networkx as nx
import parsl

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps import (
    filter_bucket_synthetic,
    finalize_synthetic,
    sort_bucket_synthetic,
    verify_sorted_bucket_synthetic,
)
from config import gen_config
from workflowbuilder import *


def build_synthetic_workflow(
    num_files,
    num_buckets,
    filter_time,
    sort_time,
    verify_time,
    finalize_time,
):
    wf = Workflow()

    filter_sort_patterns = []

    for bucket_id in range(num_buckets):
        pattern_name = f"filter_sort_bucket_{bucket_id}"
        pattern_times = [filter_time] * num_files + [sort_time]

        pattern = MapReduce(
            pattern_name,
            num_files + 1,
            pattern_times,
        )

        node_names = {
            f"{pattern_name}_{file_id}": f"filter_bucket_b{bucket_id}_f{file_id}"
            for file_id in range(num_files)
        }
        node_names[f"{pattern_name}_{num_files}"] = f"sort_bucket_{bucket_id}"
        nx.relabel_nodes(pattern.get_dag(), node_names, copy=False)

        wf.add_pattern(pattern)
        filter_sort_patterns.append(pattern_name)

    final_pattern_name = "verify_and_finalize"
    final_times = [verify_time] * num_buckets + [finalize_time]
    final_pattern = MapReduce(
        final_pattern_name,
        num_buckets + 1,
        final_times,
    )

    final_node_names = {
        f"{final_pattern_name}_{bucket_id}": f"verify_sorted_bucket_{bucket_id}"
        for bucket_id in range(num_buckets)
    }
    final_node_names[f"{final_pattern_name}_{num_buckets}"] = "finalize"
    nx.relabel_nodes(final_pattern.get_dag(), final_node_names, copy=False)
    wf.add_pattern(final_pattern)

    for bucket_id, pattern_name in enumerate(filter_sort_patterns):
        wf.add_pattern_edge(
            pattern_name,
            final_pattern_name,
            policy="target_index",
            target_index=bucket_id,
        )

    wf.set_new_root(filter_sort_patterns[0])
    wf.parse(time_as_arg=True)

    return wf


def submit_node(node, duration, inputs, work_mode):
    if node.startswith("filter_bucket_"):
        return filter_bucket_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("sort_bucket_"):
        return sort_bucket_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("verify_sorted_bucket_"):
        return verify_sorted_bucket_synthetic(node, duration, work_mode, inputs=inputs)
    if node == "finalize":
        return finalize_synthetic(node, duration, work_mode, inputs=inputs)

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
    parser.add_argument("--files", type=int, default=256)
    parser.add_argument("--buckets", type=int, default=256)
    parser.add_argument("--filter-time", type=float, default=3.04)
    parser.add_argument("--sort-time", type=float, default=65.11)
    parser.add_argument("--verify-time", type=float, default=10.04)
    parser.add_argument("--finalize-time", type=float, default=0.04)
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

    filter_time = args.filter_time * args.time_scale
    sort_time = args.sort_time * args.time_scale
    verify_time = args.verify_time * args.time_scale
    finalize_time = args.finalize_time * args.time_scale

    print(f"[INFO] files={args.files}")
    print(f"[INFO] buckets={args.buckets}")
    print(f"[INFO] filter_time={filter_time}")
    print(f"[INFO] sort_time={sort_time}")
    print(f"[INFO] verify_time={verify_time}")
    print(f"[INFO] finalize_time={finalize_time}")
    print(f"[INFO] time_scale={args.time_scale}")
    print(f"[INFO] work_mode={args.work_mode}")
    print(f"[INFO] slurm={args.onslurm}")

    start = time.time()

    try:
        workflow = build_synthetic_workflow(
            args.files,
            args.buckets,
            filter_time,
            sort_time,
            verify_time,
            finalize_time,
        )

        if args.export_pdf:
            workflow.export_pydot(filename="terasort_sintetico_workflowbuilder.pdf")

        results = run_parsl_from_workflow(workflow, args.work_mode)
        elapsed = time.time() - start

        print("\n[OK] Workflow sintetico finalizado.")
        print(f"[OK] Resultado final: {results}")
        print(f"[OK] Makespan observado: {elapsed:.2f} s")
        print(f"[OK] Total nodes: {workflow.dag_parsed.number_of_nodes()}")
        print(f"[OK] Total edges: {workflow.dag_parsed.number_of_edges()}")
        print(f"[OK] Filter tasks: {args.files * args.buckets}")
        print(f"[OK] Sort tasks: {args.buckets}")
        print(f"[OK] Verify tasks: {args.buckets}")
        print("[OK] Finalize tasks: 1")
    finally:
        parsl.dfk().cleanup()
        parsl.clear()
