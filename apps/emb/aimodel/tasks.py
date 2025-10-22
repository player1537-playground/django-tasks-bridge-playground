"""
AI Model tasks - processes non-sensitive data through AI model
"""
from django_tasks import task


@task(backend="aimodel")
def process_with_ai_model(data):
    """
    Second emb component: Processes non-sensitive data through AI model.

    In a real implementation, this would call an actual AI model.
    For this demo, it just returns a hardcoded result.

    Args:
        data: Non-sensitive data to process (should be "second-emb-request")

    Returns:
        str: Result from AI model processing
    """
    print(f"[AI Model] Received non-sensitive data: {data}")

    # In production, this would call the actual AI model
    # For demo purposes, we just return a hardcoded result
    result = "second-emb-result"

    print(f"[AI Model] Returning result: {result}")
    return result
