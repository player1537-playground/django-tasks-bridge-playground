"""
Dummy task definitions for bridge tasks.
These are stub definitions used by the web project to enqueue tasks to the bridge worker.
The actual implementation is in apps/w2e/bridge/tasks.py.
"""
from django_tasks import task


@task(backend="default", queue_name="bridge")
def web_to_emb(sensitive_data: str, return_task_id: str) -> str:
    """
    Stub for the bridge task that runs in the w2e project.
    This should never actually execute - it's only used for enqueueing.
    """
    raise NotImplementedError(
        "This task is only meant to be run on the bridge worker in the w2e project"
    )


@task(backend="default", queue_name="bridge")
def emb_to_web(ai_result: str, return_task_id: str) -> str:
    """
    Stub for the bridge callback task that runs in the w2e project.
    This should never actually execute - it's only used for enqueueing.
    """
    raise NotImplementedError(
        "This task is only meant to be run on the bridge worker in the w2e project"
    )
