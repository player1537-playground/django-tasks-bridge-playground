"""
Management command to trigger the cross-project task workflow
"""
from django.core.management.base import BaseCommand
from django_tasks import default_task_backend
import time


class Command(BaseCommand):
    help = 'Triggers the workflow: web -> bridge -> AI model -> bridge -> web'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Starting Cross-Project Task Workflow ===\n'))

        # Hardcoded sensitive data as per requirements
        sensitive_data = "first-emb-request"

        self.stdout.write(f"[Web] Enqueueing task to bridge with data: {sensitive_data}")

        # Enqueue task to bridge component
        # We enqueue directly to the default backend (redis-web) with the task name
        # that the bridge worker in the emb project expects
        task_result = default_task_backend.enqueue(
            "bridge.tasks.process_sensitive_data",
            args=[sensitive_data],
            kwargs={}
        )

        self.stdout.write(f"[Web] Task enqueued with ID: {task_result.id}")
        self.stdout.write("[Web] Waiting for result...")

        # Poll for the result
        max_wait = 30  # seconds
        start_time = time.time()
        while time.time() - start_time < max_wait:
            result = task_result.refresh()
            if result.is_complete:
                if result.is_failed:
                    self.stdout.write(self.style.ERROR(f"\n[Web] Task failed: {result.exception_class}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"\n[Web] Received final result: {result.result}"))
                self.stdout.write(self.style.SUCCESS('\n=== Workflow Complete ===\n'))
                return
            time.sleep(0.5)

        self.stdout.write(self.style.WARNING(f"\n[Web] Task did not complete within {max_wait} seconds"))
        self.stdout.write(self.style.WARNING("Make sure the bridge and AI model workers are running!"))
