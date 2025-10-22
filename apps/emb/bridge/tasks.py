"""
Bridge tasks - converts sensitive data to non-sensitive data
"""
from django_tasks import task
from aimodel.tasks import process_with_ai_model


@task(backend="bridge")
def process_sensitive_data(sensitive_data):
    """
    First emb component: Bridge that receives sensitive data,
    de-sensitizes it, and forwards to AI model component.

    Args:
        sensitive_data: Sensitive data from web project (should be "first-emb-request")

    Returns:
        str: Result from AI model processing
    """
    print(f"[Bridge] Received sensitive data: {sensitive_data}")

    # De-sensitize the data
    non_sensitive_data = "second-emb-request"
    print(f"[Bridge] De-sensitized data: {non_sensitive_data}")

    # Enqueue task to second emb component (AI model)
    print(f"[Bridge] Enqueueing task to AI model component")
    result = process_with_ai_model(non_sensitive_data)

    print(f"[Bridge] Received result from AI model: {result}")
    return result
