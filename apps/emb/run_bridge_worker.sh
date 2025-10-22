#!/bin/bash
# Worker script for bridge component
# Listens to redis-web (port 6379) for tasks from web project

echo "Starting Bridge Worker (listening to redis-web on port 6379)..."
python manage.py runtasks --backend bridge
