"""
AI Model tasks - processes non-sensitive data through AI model
"""
from django_tasks import task
from foobar_w2e.tasks import emb_to_web


@task(backend="emb", queue_name="emb")
def process_with_ai_model(data: str, return_task_id: str):
    """
    Processes non-sensitive data through AI model and triggers callback.

    In a real implementation, this would call an actual AI model.
    For this demo, it just returns a hardcoded result and enqueues the callback.

    Args:
        data: Non-sensitive data to process (should be "second-emb-request")
        return_task_id: Task ID in web project to send results back to

    Returns:
        str: Result from AI model processing
    """
    print(f"[AI Model] Received non-sensitive data: {data}")
    print(f"[AI Model] Return task ID: {return_task_id}")

    # In production, this would call the actual AI model
    # For demo purposes, we just return a hardcoded result
    result = "second-emb-result"

    print(f"[AI Model] Returning result: {result}")

    # Enqueue callback to bridge to send result back to web
    print(f"[AI Model] Enqueueing callback to bridge")
    emb_to_web.enqueue(result, return_task_id)

    return result
