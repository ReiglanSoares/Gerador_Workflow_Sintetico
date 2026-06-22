from workflowbuilder import *

wf = Workflow()

N_FRAGMENTS = 96
ITERATIONS = 10

KMEANS_FRAGMENT_TIME = 51.76
REDUCE_UPDATE_TIME = 0.09

previous_reduce = None

for it in range(ITERATIONS):

    fragments = []

    for frag in range(N_FRAGMENTS):
        frag_name = f"kmeans_fragment_it{it}_frag{frag}"

        wf.add_pattern(SingleTask(
            frag_name,
            KMEANS_FRAGMENT_TIME
        ))

        fragments.append(frag_name)

        if previous_reduce is not None:
            wf.add_pattern_edge(previous_reduce, frag_name)

    reduce_name = f"reduce_and_update_it{it}"

    wf.add_pattern(SingleTask(
        reduce_name,
        REDUCE_UPDATE_TIME
    ))

    for frag_name in fragments:
        wf.add_pattern_edge(frag_name, reduce_name)

    previous_reduce = reduce_name

wf.set_new_root("kmeans_fragment_it0_frag0")

tasks_definitions, tasks_calls = wf.parse()

wf.export_pydot()
