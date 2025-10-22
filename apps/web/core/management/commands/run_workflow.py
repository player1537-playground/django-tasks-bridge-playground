"""
Management command to trigger the cross-project task workflow

NOTE: This command requires USE_REDIS=1 to work, as it enqueues tasks
by name string to be picked up by workers in another project.
"""
from django.core.management.base import BaseCommand
import django_rq
import time
import os


class Command(BaseCommand):
    help = 'Triggers the workflow: web -> bridge -> AI model -> bridge -> web'

    def handle(self, *args, **options):
        if not os.environ.get('USE_REDIS'):
            self.stdout.write(self.style.ERROR(
                '\nERROR: This command requires USE_REDIS=1 to be set.\n'
                'Cross-project task enqueueing requires Redis.\n'
                '\nFor testing the workflow, use: apps/emb/test_workflow.py\n'
            ))
            return

        self.stdout.write(self.style.SUCCESS('\n=== Starting Cross-Project Task Workflow ===\n'))

        # Hardcoded sensitive data as per requirements
        sensitive_data = "first-emb-request"

        self.stdout.write(f"[Web] Enqueueing task to bridge with data: {sensitive_data}")

        # Enqueue task to bridge queue using RQ directly
        # The bridge worker in the emb project will pick this up
        # We need to access the .func attribute to get the actual callable
        queue = django_rq.get_queue('bridge')
        job = queue.enqueue(
            'bridge.tasks.process_sensitive_data.func',
            sensitive_data,
        )

        self.stdout.write(f"[Web] Task enqueued with ID: {job.id}")
        self.stdout.write("[Web] Waiting for result...")

        # Poll for the result
        max_wait = 30  # seconds
        start_time = time.time()
        while time.time() - start_time < max_wait:
            job.refresh()
            if job.is_finished:
                result = job.return_value()
                self.stdout.write(self.style.SUCCESS(f"\n[Web] Received final result: {result}"))
                self.stdout.write(self.style.SUCCESS('\n=== Workflow Complete ===\n'))
                return
            elif job.is_failed:
                self.stdout.write(self.style.ERROR(f"\n[Web] Task failed: {job.exc_info}"))
                return
            time.sleep(0.5)

        self.stdout.write(self.style.WARNING(f"\n[Web] Task did not complete within {max_wait} seconds"))
        self.stdout.write(self.style.WARNING("Make sure the bridge and AI model workers are running!"))
