#!/usr/bin/env python
"""
Test script to verify the task workflow logic works correctly.
This tests the emb project's bridge and AI model tasks locally.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emb.settings')
django.setup()

from bridge.tasks import process_sensitive_data
from aimodel.tasks import process_with_ai_model

print("=== Testing Django Tasks Bridge Workflow ===\n")

# Test AI model task directly
print("1. Testing AI model task directly...")
task_result = process_with_ai_model.enqueue("second-emb-request")
print(f"   Task enqueued with ID: {task_result.id}")
print(f"   Waiting for result...")
result = task_result.return_value
print(f"   Result: {result}")
assert result == "second-emb-result", f"Expected 'second-emb-result', got '{result}'"
print("   ✓ AI model task works correctly\n")

# Test bridge task (which calls AI model)
print("2. Testing bridge task (which calls AI model)...")
task_result = process_sensitive_data.enqueue("first-emb-request")
print(f"   Task enqueued with ID: {task_result.id}")
print(f"   Waiting for result...")
result = task_result.return_value
print(f"   Result: {result}")
assert result == "second-emb-result", f"Expected 'second-emb-result', got '{result}'"
print("   ✓ Bridge task works correctly\n")

print("=== All Tests Passed ===")
print("\nNote: These tests run synchronously. In production with Redis,")
print("tasks would be queued and processed asynchronously by workers.")
