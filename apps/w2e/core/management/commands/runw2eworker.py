"""
Custom management command to run the w2e worker with preconfigured settings.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run the w2e worker with preconfigured job class and queue'

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-scheduler',
            action='store_true',
            dest='with_scheduler',
            default=True,
            help='Run worker with scheduler (default: True)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting w2e worker on queue "w2e"...')
        )

        # Call rqworker with preconfigured settings
        call_command(
            'rqworker',
            'w2e',
            '--job-class', 'django_tasks.backends.rq.Job',
            '--with-scheduler' if options['with_scheduler'] else None,
        )
