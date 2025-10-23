"""
Task definitions for web project
"""
from django_tasks import task


@task()
def enqueue_to_bridge(sensitive_data):
    """
    Enqueues a task to the bridge component in the emb project.

    This is a placeholder task definition that allows the web project
    to enqueue tasks that will be processed by the bridge component
    in the emb project.

    Both projects share the same redis-web queue, so tasks enqueued here
    will be picked up by bridge workers in the emb project.

    Args:
        sensitive_data: Sensitive data to send to bridge

    Returns:
        str: Result from the bridge/AI model processing
    """
    # This function definition is never actually called
    # It exists only to provide the task signature for enqueueing
    # The actual implementation is in apps/emb/bridge/tasks.py
    pass
