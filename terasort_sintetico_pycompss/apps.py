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
def filter_bucket_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "filter_bucket",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def sort_bucket_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "sort_bucket",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def verify_sorted_bucket_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "verify_sorted_bucket",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def finalize_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "finalize",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }
