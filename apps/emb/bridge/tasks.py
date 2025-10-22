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
    task_result = process_with_ai_model.enqueue(non_sensitive_data)

    # Wait for the result (this blocks until the task completes)
    import time
    max_wait = 30
    start_time = time.time()
    while time.time() - start_time < max_wait:
        task_result.refresh()
        if task_result.is_finished:
            result = task_result.return_value
            print(f"[Bridge] Received result from AI model: {result}")
            return result
        time.sleep(0.5)

    raise TimeoutError("AI model task did not complete within 30 seconds")
