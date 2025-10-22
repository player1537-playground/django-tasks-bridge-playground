#!/bin/bash
# Worker script for AI model component
# Listens to redis-emb (port 6380) for tasks from bridge component

echo "Starting AI Model Worker (listening to redis-emb on port 6380)..."
python manage.py runtasks --backend aimodel
