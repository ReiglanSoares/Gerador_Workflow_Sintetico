from parsl import python_app


@python_app
def wordcount_bucketed_synthetic(task_name, duration, inputs=[]):
    import time

    start = time.time()
    time.sleep(duration)
    end = time.time()

    return {
        "task": "wordcount_bucketed",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }


@python_app
def reduce_bucket_synthetic(task_name, duration, inputs=[]):
    import time

    start = time.time()
    time.sleep(duration)
    end = time.time()

    return {
        "task": "reduce_bucket",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }
  @python_app
def merge_outputs_synthetic(task_name, duration, inputs=[]):
    import time

    start = time.time()
    time.sleep(duration)
    end = time.time()

    return {
        "task": "merge_outputs",
        "task_name": task_name,
        "duration": duration,
        "elapsed": end - start,
        "num_inputs": len(inputs),
    }
