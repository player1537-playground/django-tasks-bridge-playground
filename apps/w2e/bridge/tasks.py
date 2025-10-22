"""
Bridge tasks - converts sensitive data to non-sensitive data
"""
from django_tasks import task, task_backends
from django_tasks.base import Task, TaskResult
from dataclasses import dataclass
import time


# External task reference for cross-project enqueueing
# This references the aimodel task without importing it
def _external_aimodel_task_placeholder(data: str) -> str:
    """
    Placeholder function that represents the external aimodel task.
    This is never actually called - it's only used to create a Task reference.
    """
    raise NotImplementedError("This is a placeholder for cross-project task reference")


# Create a task reference to the external aimodel.tasks.process_with_ai_model
# We override the module_path property to point to the actual external task
# We also override __post_init__ to skip validation since this is a cross-project reference
@dataclass(frozen=True)
class ExternalTaskReference(Task):
    """A Task reference that points to an external module path"""
    _external_module_path: str = ""

    def __post_init__(self) -> None:
        # Skip validation for external task references
        pass

    @property
    def module_path(self) -> str:
        return self._external_module_path or super().module_path


# Create task reference for the aimodel task
aimodel_task_ref = ExternalTaskReference(
    func=_external_aimodel_task_placeholder,
    priority=0,
    backend="aimodel",
    queue_name="aimodel",
    run_after=None,
    enqueue_on_commit=None,
    takes_context=False,
    _external_module_path="aimodel.tasks.process_with_ai_model"
)


@task(backend="bridge")
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

    # Enqueue task to emb AI model using django-tasks RQ backend
    print(f"[W2E Bridge] Enqueueing task to emb AI model")
    backend = task_backends['aimodel']
    task_result: TaskResult = backend.enqueue(
        aimodel_task_ref,
        args=(non_sensitive_data,),
        kwargs={}
    )

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
