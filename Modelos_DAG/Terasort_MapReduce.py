import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflowbuilder import *

wf = Workflow()

NUM_TOP_PATTERNS = 4
TASKS_PER_PATTERN = 5
TASK_TIME = 1

top_patterns = []

for i in range(NUM_TOP_PATTERNS):
    pattern_name = f"mapreduce_top_{i}"
    wf.add_pattern(MapReduce(pattern_name, TASKS_PER_PATTERN, TASK_TIME))
    top_patterns.append(pattern_name)

wf.add_pattern(MapReduce("mapreduce_final", TASKS_PER_PATTERN, TASK_TIME))

for target_index, pattern_name in enumerate(top_patterns):
    wf.add_pattern_edge(
        pattern_name,
        "mapreduce_final",
        policy="target_index",
        target_index=target_index,
    )

wf.set_new_root("mapreduce_top_0")

tasks_definitions, tasks_calls = wf.parse()

wf.export_pydot(filename="dag_terasort.pdf")
