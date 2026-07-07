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
def init_centroids_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "init_centroids",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def kmeans_fragment_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "kmeans_fragment",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def reduce_and_update_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "reduce_and_update",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@task(inputs=COLLECTION_IN, returns=1)
def finalize_kmeans_synthetic(task_name, duration, work_mode="sleep", inputs=[]):
    import time

    start = time.time()
    _simulate_duration(duration, work_mode)
    end = time.time()

    return {
        "task": "finalize_kmeans",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }
