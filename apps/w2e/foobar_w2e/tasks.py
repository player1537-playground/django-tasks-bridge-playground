"""
W2E tasks - handles data flow between web and embedding projects
"""
from django_tasks import task
from foobar_emb.tasks import process_with_ai_model


@task(backend="w2e", queue_name="w2e")
def web_to_emb(sensitive_data: str, return_task_id: str):
    """
    W2E: Receives sensitive data from web project,
    de-sensitizes it, and forwards to emb AI model.

    Args:
        sensitive_data: Sensitive data from web project (should be "first-emb-request")
        return_task_id: The task ID to send results back to in the web project

    Returns:
        str: Task ID of the emb task (for tracking)
    """
    print(f"[W2E -> EMB] Received sensitive data: {sensitive_data}")
    print(f"[W2E -> EMB] Return task ID: {return_task_id}")

    # De-sensitize the data
    non_sensitive_data = "second-emb-request"
    print(f"[W2E -> EMB] De-sensitized data: {non_sensitive_data}")

    # Enqueue task to emb AI model with callback information
    print(f"[W2E -> EMB] Enqueueing task to emb AI model")
    task_result = process_with_ai_model.enqueue(
        non_sensitive_data,
        return_task_id
    )

    print(f"[W2E -> EMB] Enqueued to emb with ID: {task_result.id}")
    return task_result.id


@task(backend="w2e", queue_name="w2e")
def emb_to_web(ai_result: str, return_task_id: str):
    """
    W2E: Receives result from emb AI model and sends it back to web.

    Args:
        ai_result: Result from AI model processing
        return_task_id: The task ID in web project to update with the result

    Returns:
        str: Confirmation message
    """
    print(f"[W2E <- EMB] Received AI result: {ai_result}")
    print(f"[W2E <- EMB] Sending result back to web task: {return_task_id}")

    # In a real implementation, this would update the web project's task result
    # For now, we'll just print and return
    # TODO: Implement cross-project result delivery mechanism

    print(f"[W2E <- EMB] Result delivered to web")
    return f"Delivered result to web task {return_task_id}: {ai_result}"
