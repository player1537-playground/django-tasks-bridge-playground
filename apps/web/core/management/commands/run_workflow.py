"""
Management command to trigger the cross-project task workflow
"""
from django.core.management.base import BaseCommand
from bridge.tasks import process_sensitive_data
import time


class Command(BaseCommand):
    help = 'Triggers the workflow: web -> bridge -> AI model -> bridge -> web'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Starting Cross-Project Task Workflow ===\n'))

        # Hardcoded sensitive data as per requirements
        sensitive_data = "first-emb-request"

        self.stdout.write(f"[Web] Enqueueing task to bridge with data: {sensitive_data}")

        # Enqueue task to bridge using django-tasks API
        # The bridge worker in the w2e project will pick this up
        task_result = process_sensitive_data.enqueue(sensitive_data)

        self.stdout.write(f"[Web] Task enqueued with ID: {task_result.id}")
        self.stdout.write("[Web] Waiting for result...")

        # Poll for the result
        max_wait = 30  # seconds
        start_time = time.time()
        while time.time() - start_time < max_wait:
            task_result = task_result.refresh()
            if task_result.is_finished:
                if task_result.is_failed:
                    self.stdout.write(self.style.ERROR(f"\n[Web] Task failed: {task_result.exception_class}"))
                    return
                result = task_result.return_value
                self.stdout.write(self.style.SUCCESS(f"\n[Web] Received final result: {result}"))
                self.stdout.write(self.style.SUCCESS('\n=== Workflow Complete ===\n'))
                return
            time.sleep(0.5)

        self.stdout.write(self.style.WARNING(f"\n[Web] Task did not complete within {max_wait} seconds"))
        self.stdout.write(self.style.WARNING("Make sure the bridge and AI model workers are running!"))
