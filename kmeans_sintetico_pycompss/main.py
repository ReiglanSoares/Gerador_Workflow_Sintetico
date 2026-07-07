import argparse
import sys
import time
from pathlib import Path

import networkx as nx
from pycompss.api.api import compss_wait_on

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps import (
    finalize_kmeans_synthetic,
    init_centroids_synthetic,
    kmeans_fragment_synthetic,
    reduce_and_update_synthetic,
)
from workflowbuilder import *


def build_synthetic_workflow(
    num_fragments,
    iterations,
    init_time,
    fragment_time,
    reduce_time,
    finalize_time,
):
    wf = Workflow()

    init_name = "init_centroids"
    wf.add_pattern(SingleTask(init_name, init_time))

    previous_step = init_name

    for it in range(iterations):
        iteration_name = f"kmeans_iteration_it{it}"
        iteration_times = [fragment_time] * num_fragments + [reduce_time]

        iteration_pattern = MapReduce(
            iteration_name,
            num_fragments + 1,
            iteration_times,
        )

        node_names = {
            f"{iteration_name}_{frag}": f"kmeans_fragment_it{it}_frag{frag}"
            for frag in range(num_fragments)
        }
        node_names[f"{iteration_name}_{num_fragments}"] = f"reduce_and_update_centroids_it{it}"
        nx.relabel_nodes(iteration_pattern.get_dag(), node_names, copy=False)

        wf.add_pattern(iteration_pattern)
        wf.add_pattern_edge(previous_step, iteration_name)

        previous_step = iteration_name

    finalize_name = "finalize_kmeans"
    wf.add_pattern(SingleTask(finalize_name, finalize_time))
    wf.add_pattern_edge(previous_step, finalize_name)

    wf.set_new_root(init_name)
    wf.parse(time_as_arg=True)

    return wf


def submit_node(node, duration, inputs, work_mode):
    if node.startswith("init_centroids_"):
        return init_centroids_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("kmeans_fragment_"):
        return kmeans_fragment_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("reduce_and_update_centroids_"):
        return reduce_and_update_synthetic(node, duration, work_mode, inputs=inputs)
    if node.startswith("finalize_kmeans_"):
        return finalize_kmeans_synthetic(node, duration, work_mode, inputs=inputs)

    raise ValueError(f"Unknown synthetic task type for node: {node}")


def run_pycompss_from_workflow(wf, work_mode):
    futures = {}

    for node in nx.topological_sort(wf.dag_parsed):
        parents = list(wf.dag_parsed.predecessors(node))
        inputs = [futures[parent] for parent in parents]
        duration = wf.dag_parsed.nodes[node].get("time", 1)
        futures[node] = submit_node(node, duration, inputs, work_mode)

    sink_nodes = [node for node in wf.dag_parsed.nodes if wf.dag_parsed.out_degree(node) == 0]
    return compss_wait_on([futures[node] for node in sink_nodes])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fragments", type=int, default=1056)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--init-time", type=float, default=0.720)
    parser.add_argument("--fragment-time", type=float, default=44.612)
    parser.add_argument("--reduce-time", type=float, default=1.386)
    parser.add_argument("--finalize-time", type=float, default=0.069)
    parser.add_argument("--time-scale", type=float, default=1.0)
    parser.add_argument("--work-mode", choices=["sleep", "cpu"], default="sleep")
    parser.add_argument("--export-pdf", action="store_true")
    args = parser.parse_args()

    init_time = args.init_time * args.time_scale
    fragment_time = args.fragment_time * args.time_scale
    reduce_time = args.reduce_time * args.time_scale
    finalize_time = args.finalize_time * args.time_scale

    print(f"[INFO] fragments={args.fragments}")
    print(f"[INFO] iterations={args.iterations}")
    print(f"[INFO] init_time={init_time}")
    print(f"[INFO] fragment_time={fragment_time}")
    print(f"[INFO] reduce_time={reduce_time}")
    print(f"[INFO] finalize_time={finalize_time}")
    print(f"[INFO] time_scale={args.time_scale}")
    print(f"[INFO] work_mode={args.work_mode}")

    start = time.time()

    workflow = build_synthetic_workflow(
        args.fragments,
        args.iterations,
        init_time,
        fragment_time,
        reduce_time,
        finalize_time,
    )

    if args.export_pdf:
        workflow.export_pydot(filename="kmeans_sintetico_pycompss_workflowbuilder.pdf")

    results = run_pycompss_from_workflow(workflow, args.work_mode)
    elapsed = time.time() - start

    print("\n[OK] Workflow sintetico finalizado.")
    print(f"[OK] Resultado final: {results}")
    print(f"[OK] Makespan observado: {elapsed:.2f} s")
    print(f"[OK] Total nodes: {workflow.dag_parsed.number_of_nodes()}")
    print(f"[OK] Total edges: {workflow.dag_parsed.number_of_edges()}")
    print("[OK] Init tasks: 1")
    print(f"[OK] KMeans fragment tasks: {args.fragments * args.iterations}")
    print(f"[OK] Reduce/update tasks: {args.iterations}")
    print("[OK] Finalize tasks: 1")
