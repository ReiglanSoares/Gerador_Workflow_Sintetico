from workflowbuilder import *

wf = Workflow()

NUM_FILES = 4
NUM_BUCKETS = 4

FILTER_TIME = 20
SORT_TIME = 30
VERIFY_TIME = 2
FINALIZE_TIME = 1

filter_tasks_by_bucket = {}

for bid in range(NUM_BUCKETS):
    filter_tasks_by_bucket[bid] = []

    for fid in range(NUM_FILES):
        task_name = f"filter_bucket_b{bid}_f{fid}"

        wf.add_pattern(SingleTask(
            task_name,
            FILTER_TIME
        ))

        filter_tasks_by_bucket[bid].append(task_name)

sort_tasks = []

for bid in range(NUM_BUCKETS):
    sort_name = f"sort_bucket_{bid}"

    wf.add_pattern(SingleTask(
        sort_name,
        SORT_TIME
    ))

    for filter_task in filter_tasks_by_bucket[bid]:
        wf.add_pattern_edge(filter_task, sort_name)

    sort_tasks.append(sort_name)
verify_tasks = []

for bid in range(NUM_BUCKETS):
    verify_name = f"verify_sorted_bucket_{bid}"

    wf.add_pattern(SingleTask(
        verify_name,
        VERIFY_TIME
    ))

    wf.add_pattern_edge(sort_tasks[bid], verify_name)

    verify_tasks.append(verify_name)

wf.add_pattern(SingleTask(
    "finalize",
    FINALIZE_TIME
))

for verify_task in verify_tasks:
    wf.add_pattern_edge(verify_task, "finalize")

wf.set_new_root("filter_bucket_b0_f0")

tasks_definitions, tasks_calls = wf.parse()

wf.export_pydot()
