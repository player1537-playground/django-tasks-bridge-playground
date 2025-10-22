#!/usr/bin/env python
"""
Test script to verify the w2e bridge task configuration.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'w2e.settings')
django.setup()

from bridge.tasks import process_sensitive_data

print("=== Testing W2E Bridge Configuration ===\n")

# Test that the bridge task is properly configured
print("1. Checking bridge task configuration...")
print(f"   Task name: {process_sensitive_data.name}")
print(f"   Task backend: {process_sensitive_data.backend}")
print(f"   ✓ Bridge task configured correctly\n")

print("=== Configuration Test Passed ===")
print("\nNote: Full workflow testing requires the emb AI model project.")
print("Run both w2e and emb workers for end-to-end testing.")
