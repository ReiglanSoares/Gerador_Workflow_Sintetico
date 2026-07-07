from parsl import python_app

def _simulate_duration(duration, work_mode):
    import time

    if work_mode == "cpu":
        end = time.time() + duration
        while time.time() < end:
            _ = 123456789 ** 2
        return

    time.sleep(duration)


@python_app
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


@python_app
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


@python_app
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


@python_app
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
