# Django Tasks Cross-Project Workflow

This project demonstrates a working cross-project Django Tasks workflow with three separate Django projects communicating via Redis task queues.

## Architecture

```
┌─────────┐         ┌──────────┐         ┌─────────┐
│   Web   │────────▶│   W2E    │────────▶│   EMB   │
│ Project │         │  Bridge  │         │ Project │
└─────────┘         └──────────┘         └─────────┘
     │                    ▲                     │
     │                    │                     │
     └────────────────────┴─────────────────────┘
                  (async callbacks)

Redis-Web (6379)           Redis-EMB (6380)
     bridge queue              aimodel queue
```

## Data Flow

1. **Web → Bridge** (`web_to_emb`)
   - Web project sends "first-emb-request" (sensitive data)
   - Bridge receives and de-sensitizes to "second-emb-request"
   - Bridge enqueues to AI model queue

2. **Bridge → AI Model** (`process_with_ai_model`)
   - AI model processes "second-emb-request"
   - Returns "second-emb-result"
   - Enqueues callback to bridge

3. **AI Model → Bridge** (`emb_to_web` callback)
   - Bridge receives AI result
   - Delivers result back to web (placeholder implementation)

## Key Implementation Details

### Dummy Task Pattern

Each project contains **dummy task stubs** for tasks that actually run in other projects:

- **apps/web/bridge/tasks.py**: Stubs for `web_to_emb` and `emb_to_web`
- **apps/w2e/aimodel/tasks.py**: Stub for `process_with_ai_model`
- **apps/emb/bridge/tasks.py**: Stub for `emb_to_web`

These stubs:
- Use the `@task` decorator with proper backend/queue configuration
- Raise `NotImplementedError` (never actually execute)
- Allow cross-project task enqueueing using public django-tasks API

### Backend Configuration

Each project configures multiple backends to enqueue to different Redis instances:

```python
TASKS = {
    "default": {...},
    "bridge": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["bridge"],
    },
    "aimodel": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
        "QUEUES": ["aimodel"],
    },
}
```

### Worker Configuration

Workers must use the django-tasks custom Job class:

```bash
python manage.py rqworker bridge --with-scheduler --job-class django_tasks.backends.rq.Job
```

## Running the Workflow

1. **Start Redis instances:**
   ```bash
   redis-server --port 6379 --daemonize yes
   redis-server --port 6380 --daemonize yes
   ```

2. **Start workers:**
   ```bash
   # W2E Bridge worker
   cd apps/w2e
   ./run_worker.sh

   # EMB AI Model worker
   cd apps/emb
   ./run_worker.sh
   ```

3. **Trigger workflow:**
   ```bash
   cd apps/web
   python manage.py run_workflow
   ```

4. **Check worker logs** to see the complete flow:
   - Web → Bridge: De-sensitization
   - Bridge → AI Model: Processing
   - AI Model → Bridge: Callback
   - Bridge → Web: Result delivery

## Success Criteria

✅ Workers use correct Job class for Task objects
✅ Cross-project task enqueueing via dummy stubs
✅ Async callback architecture (no polling)
✅ Tasks execute across three separate projects
✅ Data flows through two Redis instances
✅ Uses only public django-tasks API
✅ No internal django-tasks hacks or workarounds

## Output Example

```
=== Starting Cross-Project Task Workflow ===
[Web] Sensitive data: first-emb-request
[Web] Return task ID: web-placeholder-task-123
[Web] Enqueueing task to bridge...
[Web] Task enqueued with ID: eA0Gl7R9PzaljR9RhO8d32LuQPCCDoBO
[Web] Workflow initiated successfully!

# W2E Worker Log:
[W2E Bridge -> EMB] Received sensitive data: first-emb-request
[W2E Bridge -> EMB] De-sensitized data: second-emb-request
[W2E Bridge -> EMB] Enqueued to aimodel with ID: rSRF2lp0lxexxXznrRT5rjj568NgtccB

# EMB Worker Log:
[AI Model] Received non-sensitive data: second-emb-request
[AI Model] Returning result: second-emb-result
[AI Model] Enqueueing callback to bridge

# W2E Worker Log:
[W2E Bridge <- EMB] Received AI result: second-emb-result
[W2E Bridge <- EMB] Result delivered to web
```

## Implementation Notes

- Uses `uv` for package management with editable django-tasks install from source
- Minimal Django configurations (no web serving, tasks-only)
- SQLite for local development (Postgres commented out for production)
- RQ backend with two separate Redis instances for queue isolation
- Async/callback pattern avoids cross-backend result polling issues
