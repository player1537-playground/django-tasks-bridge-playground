#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'w2e.settings')

print("=== Debug Worker Environment ===")
print("1. Before django.setup():")

import django
django.setup()

print("\n2. After django.setup():")
from django.conf import settings
print(f"TASKS config: {settings.TASKS}")

from django_tasks import task_backends
print(f"\n3. Backend queues:")
print(f"  bridge: {task_backends['bridge'].queues}")

print(f"\n4. Trying to import bridge.tasks...")
try:
    from bridge import tasks
    print(f"  SUCCESS!")
    print(f"  process_sensitive_data: {tasks.process_sensitive_data}")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()
