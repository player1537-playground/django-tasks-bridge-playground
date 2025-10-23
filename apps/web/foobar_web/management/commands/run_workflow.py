"""
Management command to trigger the cross-project task workflow
"""
from django.core.management.base import BaseCommand
from foobar_w2e.tasks import web_to_emb


class Command(BaseCommand):
    help = 'Triggers the workflow: web -> bridge -> AI model -> bridge -> web'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Starting Cross-Project Task Workflow ===\n'))

        # Hardcoded sensitive data as per requirements
        sensitive_data = "first-emb-request"

        # Create a placeholder task ID for tracking the return path
        # In a real implementation, this would be a real task that waits for results
        return_task_id = "web-placeholder-task-123"

        self.stdout.write(f"[Web] Sensitive data: {sensitive_data}")
        self.stdout.write(f"[Web] Return task ID: {return_task_id}")
        self.stdout.write(f"[Web] Enqueueing task to bridge...")

        # Enqueue task to bridge using django-tasks API
        # The bridge worker in the w2e project will pick this up
        task_result = web_to_emb.enqueue(sensitive_data, return_task_id)

        self.stdout.write(f"[Web] Task enqueued with ID: {task_result.id}")
        self.stdout.write(self.style.SUCCESS('\n[Web] Workflow initiated successfully!'))
        self.stdout.write('\nNote: This is an async workflow.')
        self.stdout.write('Check worker logs to see the full flow:')
        self.stdout.write('  1. Web -> Bridge (web_to_emb)')
        self.stdout.write('  2. Bridge -> AI Model (process_with_ai_model)')
        self.stdout.write('  3. AI Model -> Bridge (emb_to_web callback)')
        self.stdout.write('  4. Bridge -> Web (result delivery)\n')
