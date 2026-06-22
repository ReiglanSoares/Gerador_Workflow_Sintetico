from workflowbuilder import *

wf = Workflow()

NUM_FILES = 8
NUM_BUCKETS = 8

WORDCOUNT_TIME = 355.96
REDUCE_TIME = 814.16
MERGE_TIME = 1

maps = []

for i in range(NUM_FILES):
    name = f"wordcount_bucketed_{i}"
    wf.add_pattern(SingleTask(name, WORDCOUNT_TIME))
    maps.append(name)

final_buckets = []

for b in range(NUM_BUCKETS):

    current_level = maps.copy()

    round_id = 1

    while len(current_level) > 1:
        next_level = []

        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1]

            reduce_name = f"reduce_bucket_b{b}_r{round_id}_{i//2}"

            wf.add_pattern(SingleTask(reduce_name, REDUCE_TIME))

            wf.add_pattern_edge(left, reduce_name)
            wf.add_pattern_edge(right, reduce_name)

            next_level.append(reduce_name)

        current_level = next_level
        round_id += 1

    final_buckets.append(current_level[0])

wf.add_pattern(SingleTask("merge_outputs", MERGE_TIME))
for bucket_final in final_buckets:
    wf.add_pattern_edge(bucket_final, "merge_outputs")

wf.set_new_root("wordcount_bucketed_0")

tasks_definitions, tasks_calls = wf.parse()

wf.export_pydot()
