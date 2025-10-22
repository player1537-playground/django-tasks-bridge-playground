"""
Bridge tasks - converts sensitive data to non-sensitive data
"""
from django_tasks import task
from aimodel.tasks import process_with_ai_model
import time


@task(backend="bridge", queue_name="bridge")
def process_sensitive_data(sensitive_data):
    """
    W2E Bridge: Receives sensitive data from web project,
    de-sensitizes it, and forwards to emb AI model.

    Args:
        sensitive_data: Sensitive data from web project (should be "first-emb-request")

    Returns:
        str: Result from AI model processing
    """
    print(f"[W2E Bridge] Received sensitive data: {sensitive_data}")

    # De-sensitize the data
    non_sensitive_data = "second-emb-request"
    print(f"[W2E Bridge] De-sensitized data: {non_sensitive_data}")

    # Enqueue task to emb AI model using the dummy task reference
    print(f"[W2E Bridge] Enqueueing task to emb AI model")
    task_result = process_with_ai_model.enqueue(non_sensitive_data)

    # Wait for the result (this blocks until the task completes)
    max_wait = 30
    start_time = time.time()
    while time.time() - start_time < max_wait:
        task_result = task_result.refresh()
        if task_result.is_finished:
            if task_result.is_failed:
                print(f"[W2E Bridge] AI model task failed: {task_result.exception_class}")
                raise Exception(f"AI model task failed: {task_result.exception_class}")
            result = task_result.return_value
            print(f"[W2E Bridge] Received result from AI model: {result}")
            return result
        time.sleep(0.5)

    raise TimeoutError("AI model task did not complete within 30 seconds")
