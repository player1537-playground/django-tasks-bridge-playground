"""
Dummy task definitions for aimodel tasks.
These are stub definitions used by the w2e bridge to enqueue tasks to the aimodel worker.
The actual implementation is in apps/emb/aimodel/tasks.py.
"""
from django_tasks import task


@task(backend="aimodel", queue_name="aimodel")
def process_with_ai_model(data: str) -> str:
    """
    Stub for the AI model task that runs in the emb project.
    This should never actually execute - it's only used for enqueueing.
    """
    raise NotImplementedError(
        "This task is only meant to be run on the aimodel worker in the emb project"
    )
