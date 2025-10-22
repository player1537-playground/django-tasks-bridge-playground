#!/bin/bash
# Worker script for AI model component
# Listens to redis-emb (port 6380) for tasks from w2e bridge

echo "Starting EMB AI Model Worker (listening to redis-emb on port 6380)..."
python manage.py rqworker aimodel --with-scheduler
