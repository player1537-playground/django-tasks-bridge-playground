#!/bin/bash
# Worker script for w2e bridge component
# Listens to redis-web (port 6379) for tasks from web project

echo "Starting W2E Bridge Worker (listening to redis-web on port 6379)..."
python manage.py rqworker bridge --with-scheduler
