from pycompss.api.parameter import COLLECTION_IN
from pycompss.api.task import task


def _simulate_duration(duration, work_mode):
    import time

    if work_mode == "cpu":
        end = time.time() + duration
        while time.time() < end:
            _ = 123456789 ** 2
        return

    time.sleep(duration)


@task(inputs=COLLECTION_IN, returns=1)
def wordcount_bucketed_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "wordcount_bucketed",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }
  
@task(inputs=COLLECTION_IN, returns=1)
def reduce_bucket_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "reduce_bucket",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def merge_outputs_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "merge_outputs",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }
