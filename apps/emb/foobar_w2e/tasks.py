"""
Dummy task definitions for w2e bridge tasks.
These are stub definitions used by the emb project to enqueue callbacks to the w2e worker.
The actual implementation is in apps/w2e/foobar_w2e/tasks.py.
"""
from django_tasks import task


@task(backend="w2e", queue_name="w2e")
def emb_to_web(ai_result: str, return_task_id: str) -> str:
    """
    Stub for the w2e callback task that runs in the w2e project.
    This should never actually execute - it's only used for enqueueing.
    """
    raise NotImplementedError(
        "This task is only meant to be run on the w2e worker in the w2e project"
    )
