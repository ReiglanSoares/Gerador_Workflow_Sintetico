import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import networkx as nx

from workflowbuilder import *

wf = Workflow()

N_FRAGMENTS = 48
ITERATIONS = 3

INIT_CENTROIDS_TIME = 5.12
KMEANS_FRAGMENT_TIME = 51.76
REDUCE_UPDATE_TIME = 0.29
FINALIZE_TIME = 0.05

init_name = "init_centroids"
wf.add_pattern(SingleTask(init_name, INIT_CENTROIDS_TIME))

previous_step = init_name

for it in range(ITERATIONS):
    iteration_name = f"kmeans_iteration_it{it}"

    iteration_times = [KMEANS_FRAGMENT_TIME] * N_FRAGMENTS + [REDUCE_UPDATE_TIME]

    iteration_pattern = MapReduce(
        iteration_name,
        N_FRAGMENTS + 1,
        iteration_times,
    )

    node_names = {
        f"{iteration_name}_{frag}": f"kmeans_fragment_it{it}_frag{frag}"
        for frag in range(N_FRAGMENTS)
    }
    node_names[f"{iteration_name}_{N_FRAGMENTS}"] = f"reduce_and_update_centroids_it{it}"
    nx.relabel_nodes(iteration_pattern.get_dag(), node_names, copy=False)

    wf.add_pattern(iteration_pattern)
    wf.add_pattern_edge(previous_step, iteration_name)

    previous_step = iteration_name

finalize_name = "finalize_kmeans"
wf.add_pattern(SingleTask(finalize_name, FINALIZE_TIME))
wf.add_pattern_edge(previous_step, finalize_name)

wf.set_new_root(init_name)

tasks_definitions, tasks_calls = wf.parse()

wf.export_pydot(filename="kmeans_mapreduce.pdf")
