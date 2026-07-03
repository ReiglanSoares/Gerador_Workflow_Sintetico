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


@python_app
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


@python_app
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
