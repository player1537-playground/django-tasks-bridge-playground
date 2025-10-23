# Django Tasks Bridge Playground

A demonstration of **cross-project Django Tasks workflow** using an **async callback architecture** for handling sensitive data across isolated Django projects with separate Redis backends.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Key Concepts](#key-concepts)
- [Directory Structure](#directory-structure)
- [In-Depth Code Walkthrough](#in-depth-code-walkthrough)
  - [1. Web Project: Workflow Initiation](#1-web-project-workflow-initiation)
  - [2. W2E Project: Bridging and De-sensitization](#2-w2e-project-bridging-and-de-sensitization)
  - [3. EMB Project: AI Model Processing](#3-emb-project-ai-model-processing)
  - [4. Async Callback Flow](#4-async-callback-flow)
  - [5. Multi-Backend Configuration](#5-multi-backend-configuration)
  - [6. Custom Management Commands](#6-custom-management-commands)
  - [7. Dummy Task Stubs](#7-dummy-task-stubs)
- [Quick Start](#quick-start)
- [Expected Output](#expected-output)
- [Architecture Decisions](#architecture-decisions)

---

## Architecture Overview

This project demonstrates a **three-tier Django Tasks architecture** with isolated data stores:

```
┌─────────────────────────────────────────────────────────────────┐
│                         WEB PROJECT                             │
│  (Handles sensitive data, initiates workflows)                  │
│                                                                 │
│  Redis: redis-web (localhost:6379)                             │
│  Queue: w2e                                                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ (1) Enqueues web_to_emb task
             │     Data: "first-emb-request"
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         W2E PROJECT                             │
│  (Bridge: De-sensitizes data, routes tasks)                     │
│                                                                 │
│  Redis: redis-web (6379) for receiving from web                │
│  Redis: redis-emb (6380) for sending to emb                    │
│  Queue: w2e                                                     │
└──────┬────────────────────────────────────────────┬─────────────┘
       │                                            │
       │ (2) De-sensitizes and enqueues             │ (4) Receives callback
       │     to process_with_ai_model               │     from emb_to_web
       │     Data: "second-emb-request"             │
       │                                            │
       ▼                                            │
┌─────────────────────────────────────────────────────────────────┐
│                         EMB PROJECT                             │
│  (AI Model: Processes non-sensitive data)                       │
│                                                                 │
│  Redis: redis-emb (localhost:6380)                             │
│  Queue: emb                                                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ (3) Processes and enqueues callback
             │     to emb_to_web
             │     Data: "second-emb-result"
             │
             └──────────────┘
```

### Data Flow

1. **Web → W2E**: Web project enqueues `web_to_emb` task with sensitive data (`"first-emb-request"`)
2. **W2E → EMB**: W2E de-sensitizes data to `"second-emb-request"` and enqueues `process_with_ai_model` task
3. **EMB Processing**: EMB processes data and produces result `"second-emb-result"`
4. **EMB → W2E (Callback)**: EMB enqueues `emb_to_web` callback task back to W2E queue
5. **W2E → Web**: W2E delivers result back to web project

### Why This Architecture?

- **Data Isolation**: Sensitive data stays in web project, never reaches emb
- **Security Boundaries**: Separate Redis instances prevent cross-contamination
- **Async Callbacks**: No polling, no blocking - pure event-driven architecture
- **Scalability**: Each tier can scale independently

---

## Key Concepts

### 1. **Module Naming Convention**

All functional modules use the `foobar_` prefix to match real-world project naming:

- `foobar_web` - Web application tasks
- `foobar_w2e` - Web-to-embedding bridge tasks
- `foobar_emb` - Embedding/AI model tasks

### 2. **Centralized Settings**

Each project has settings in `core/settings.py` (not in a project-specific module):

```
apps/web/core/settings.py
apps/w2e/core/settings.py
apps/emb/core/settings.py
```

### 3. **Dummy Task Stubs**

For cross-project task enqueueing, each project includes **stub task definitions** for tasks that actually run in other projects. These stubs:
- Raise `NotImplementedError` if accidentally executed
- Provide proper task signatures for type checking
- Enable task enqueueing from different projects

### 4. **Custom Worker Commands**

Preconfigured management commands eliminate the need to remember complex arguments:
- `runw2eworker` - Runs w2e worker with correct job class and queue
- `runembworker` - Runs emb worker with correct job class and queue

---

## Directory Structure

```
django-tasks-bridge-playground/
├── apps/
│   ├── web/                          # Web project (sensitive data)
│   │   ├── core/
│   │   │   └── settings.py           # Django settings
│   │   ├── foobar_web/               # Main web module
│   │   │   ├── management/commands/
│   │   │   │   └── run_workflow.py   # Workflow trigger command
│   │   │   └── tasks.py              # Web-specific tasks
│   │   ├── foobar_w2e/               # Dummy stubs for w2e tasks
│   │   │   └── tasks.py              # Stub: web_to_emb
│   │   ├── manage.py
│   │   └── pyproject.toml
│   │
│   ├── w2e/                          # W2E bridge project
│   │   ├── core/
│   │   │   ├── settings.py           # Django settings
│   │   │   └── management/commands/
│   │   │       └── runw2eworker.py   # Custom worker command
│   │   ├── foobar_web/               # Dummy stubs for web tasks
│   │   ├── foobar_w2e/               # Main w2e bridge module
│   │   │   └── tasks.py              # Implementation: web_to_emb, emb_to_web
│   │   ├── foobar_emb/               # Dummy stubs for emb tasks
│   │   │   └── tasks.py              # Stub: process_with_ai_model
│   │   ├── manage.py
│   │   └── pyproject.toml
│   │
│   └── emb/                          # EMB AI model project
│       ├── core/
│       │   ├── settings.py           # Django settings
│       │   └── management/commands/
│       │       └── runembworker.py   # Custom worker command
│       ├── foobar_emb/               # Main emb AI module
│       │   └── tasks.py              # Implementation: process_with_ai_model
│       ├── foobar_w2e/               # Dummy stubs for w2e tasks
│       │   └── tasks.py              # Stub: emb_to_web
│       ├── manage.py
│       └── pyproject.toml
│
├── libs/
│   └── django_tasks/                 # Django-tasks from source (editable install)
│
├── docker-compose.yml                # Redis services (redis-web, redis-emb)
└── README.md
```

---

## In-Depth Code Walkthrough

### 1. Web Project: Workflow Initiation

**File**: [`apps/web/foobar_web/management/commands/run_workflow.py`](apps/web/foobar_web/management/commands/run_workflow.py)

The web project initiates the workflow with a management command:

```python
from django.core.management.base import BaseCommand
from foobar_w2e.tasks import web_to_emb

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Hardcoded sensitive data as per requirements
        sensitive_data = "first-emb-request"
        return_task_id = "web-placeholder-task-123"

        # Enqueue task to w2e bridge
        task_result = web_to_emb.enqueue(sensitive_data, return_task_id)

        self.stdout.write(f"[Web] Task enqueued with ID: {task_result.id}")
```

**Key Points**:
- Imports `web_to_emb` from `foobar_w2e.tasks` (this is a **dummy stub** in the web project)
- The actual implementation lives in the w2e project
- Uses `.enqueue()` to send task to redis-web queue
- Fire-and-forget: no blocking, no polling for results
- `return_task_id` is passed along so callbacks know where to deliver results

**Dummy Stub Location**: [`apps/web/foobar_w2e/tasks.py`](apps/web/foobar_w2e/tasks.py)

```python
from django_tasks import task

@task(backend="default", queue_name="w2e")
def web_to_emb(sensitive_data: str, return_task_id: str) -> str:
    raise NotImplementedError(
        "This task is only meant to be run on the w2e worker in the w2e project"
    )
```

This stub allows web project to **enqueue** the task without implementing it.

---

### 2. W2E Project: Bridging and De-sensitization

**File**: [`apps/w2e/foobar_w2e/tasks.py`](apps/w2e/foobar_w2e/tasks.py)

The w2e project implements two tasks: `web_to_emb` (receive from web) and `emb_to_web` (receive from emb).

#### Task 1: `web_to_emb` - Forward Flow

```python
from django_tasks import task
from foobar_emb.tasks import process_with_ai_model

@task(backend="w2e", queue_name="w2e")
def web_to_emb(sensitive_data: str, return_task_id: str):
    """
    Receives sensitive data from web, de-sensitizes it,
    and forwards to emb AI model.
    """
    print(f"[W2E -> EMB] Received sensitive data: {sensitive_data}")

    # De-sensitize the data
    non_sensitive_data = "second-emb-request"
    print(f"[W2E -> EMB] De-sensitized data: {non_sensitive_data}")

    # Enqueue to emb AI model
    task_result = process_with_ai_model.enqueue(
        non_sensitive_data,
        return_task_id
    )

    print(f"[W2E -> EMB] Enqueued to emb with ID: {task_result.id}")
    return task_result.id
```

**Key Points**:
- Decorated with `@task(backend="w2e", queue_name="w2e")`
- Receives sensitive data (`"first-emb-request"`)
- De-sensitizes to `"second-emb-request"`
- Imports `process_with_ai_model` from `foobar_emb.tasks` (another **dummy stub**)
- Enqueues to redis-emb (port 6380) via the `"emb"` backend
- Passes `return_task_id` along for callback routing

#### Task 2: `emb_to_web` - Callback Flow

```python
@task(backend="w2e", queue_name="w2e")
def emb_to_web(ai_result: str, return_task_id: str):
    """
    Receives result from emb AI model and sends it back to web.
    """
    print(f"[W2E <- EMB] Received AI result: {ai_result}")
    print(f"[W2E <- EMB] Sending result back to web task: {return_task_id}")

    # In a real implementation, this would update the web project's task result
    print(f"[W2E <- EMB] Result delivered to web")
    return f"Delivered result to web task {return_task_id}: {ai_result}"
```

**Key Points**:
- This task receives the **callback** from emb project
- Runs on w2e worker (queue "w2e" on redis-web)
- Would update web project's task result in production (TODO)

---

### 3. EMB Project: AI Model Processing

**File**: [`apps/emb/foobar_emb/tasks.py`](apps/emb/foobar_emb/tasks.py)

```python
from django_tasks import task
from foobar_w2e.tasks import emb_to_web

@task(backend="emb", queue_name="emb")
def process_with_ai_model(data: str, return_task_id: str):
    """
    Processes non-sensitive data through AI model and triggers callback.
    """
    print(f"[AI Model] Received non-sensitive data: {data}")
    print(f"[AI Model] Return task ID: {return_task_id}")

    # In production, this would call the actual AI model
    result = "second-emb-result"
    print(f"[AI Model] Returning result: {result}")

    # Enqueue callback to w2e bridge
    print(f"[AI Model] Enqueueing callback to bridge")
    emb_to_web.enqueue(result, return_task_id)

    return result
```

**Key Points**:
- Decorated with `@task(backend="emb", queue_name="emb")`
- Processes de-sensitized data (`"second-emb-request"`)
- Produces result (`"second-emb-result"`)
- **Enqueues callback** to `emb_to_web` (running on w2e worker)
- Imports `emb_to_web` from `foobar_w2e.tasks` (**dummy stub** in emb project)

**Dummy Stub Location**: [`apps/emb/foobar_w2e/tasks.py`](apps/emb/foobar_w2e/tasks.py)

```python
from django_tasks import task

@task(backend="w2e", queue_name="w2e")
def emb_to_web(ai_result: str, return_task_id: str) -> str:
    raise NotImplementedError(
        "This task is only meant to be run on the w2e worker in the w2e project"
    )
```

---

### 4. Async Callback Flow

The **key innovation** in this architecture is the async callback pattern:

**Traditional (Polling) Pattern** ❌:
```python
# BAD: Blocking, wastes resources
task_result = some_task.enqueue(data)
while not task_result.is_complete():
    time.sleep(1)
    task_result.refresh()  # ❌ Doesn't work across different Redis backends!
return task_result.result
```

**Async Callback Pattern** ✅:
```python
# GOOD: Non-blocking, event-driven
def forward_task(data, callback_id):
    result = downstream_task.enqueue(data, callback_id)
    # Don't wait! Just return the task ID
    return result.id

def downstream_task(data, callback_id):
    result = process(data)
    # Trigger callback instead of returning
    callback_task.enqueue(result, callback_id)
    return result
```

This pattern enables:
- **No polling**: Tasks don't wait for results
- **Cross-backend support**: Works even when tasks are on different Redis instances
- **Scalability**: Workers can process more tasks concurrently
- **Resilience**: Failures don't cascade

---

### 5. Multi-Backend Configuration

**File**: [`apps/w2e/core/settings.py`](apps/w2e/core/settings.py)

The w2e project bridges two Redis instances, so it configures **multiple backends**:

```python
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["default", "w2e"],
    },
    "w2e": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},  # redis-web
        "QUEUES": ["w2e"],
    },
    "emb": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},  # redis-emb
        "QUEUES": ["emb"],
    },
}

RQ_QUEUES = {
    'w2e': {
        'HOST': 'localhost',
        'PORT': 6379,  # redis-web
        'DB': 0,
    },
    'emb': {
        'HOST': 'localhost',
        'PORT': 6380,  # redis-emb
        'DB': 0,
    },
}
```

**Key Points**:
- **Three backends**: default, w2e, emb
- **Two Redis instances**:
  - `localhost:6379` (redis-web) for w2e queue
  - `localhost:6380` (redis-emb) for emb queue
- The `@task(backend="...")` decorator determines which Redis instance is used
- The `queue_name="..."` parameter determines which queue on that Redis

**Backend Selection in Tasks**:
```python
@task(backend="w2e", queue_name="w2e")  # → redis-web:6379, queue "w2e"
def web_to_emb(...):
    ...

# Inside web_to_emb:
process_with_ai_model.enqueue(...)  # → redis-emb:6380, queue "emb"
```

---

### 6. Custom Management Commands

**File**: [`apps/w2e/core/management/commands/runw2eworker.py`](apps/w2e/core/management/commands/runw2eworker.py)

Instead of requiring developers to remember:
```bash
python manage.py rqworker w2e --job-class django_tasks.backends.rq.Job --with-scheduler
```

We created a **custom management command**:

```python
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
```

**Now you can simply run**:
```bash
python manage.py runw2eworker
```

The `--job-class django_tasks.backends.rq.Job` is **critical** - it ensures RQ workers properly handle django-tasks `Task` objects instead of plain RQ jobs.

**Similar command for emb**: [`apps/emb/core/management/commands/runembworker.py`](apps/emb/core/management/commands/runembworker.py)

---

### 7. Dummy Task Stubs

**Why are dummy stubs needed?**

When project A needs to enqueue a task that runs on project B's worker, project A needs:
1. The task function signature (for type checking and parameters)
2. The `@task` decorator with correct backend/queue
3. BUT NOT the actual implementation

**Example**: Web project enqueueing to w2e worker

**In web project** [`apps/web/foobar_w2e/tasks.py`](apps/web/foobar_w2e/tasks.py):
```python
@task(backend="default", queue_name="w2e")
def web_to_emb(sensitive_data: str, return_task_id: str) -> str:
    raise NotImplementedError(
        "This task is only meant to be run on the w2e worker in the w2e project"
    )
```

This allows web project to:
```python
from foobar_w2e.tasks import web_to_emb
task_result = web_to_emb.enqueue(data, task_id)  # ✅ Works!
```

But if accidentally executed in web project:
```python
task_result = web_to_emb(data, task_id)  # ❌ Raises NotImplementedError
```

**Matrix of Dummy Stubs**:

| Project | Dummy Modules | Purpose |
|---------|---------------|---------|
| web | `foobar_w2e` | Stubs for `web_to_emb` |
| w2e | `foobar_web`<br>`foobar_emb` | Stubs for web tasks (if any)<br>Stubs for `process_with_ai_model` |
| emb | `foobar_w2e` | Stubs for `emb_to_web` |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for Redis)
- uv package manager (optional, but recommended)

### 1. Start Redis Services

```bash
docker-compose up -d
```

This starts:
- `redis-web` on port 6379
- `redis-emb` on port 6380

### 2. Install Dependencies

Each project uses `uv` with editable django-tasks from source:

```bash
# Web project
cd apps/web
uv sync

# W2E project
cd apps/w2e
uv sync

# EMB project
cd apps/emb
uv sync
```

### 3. Run Workers

**Terminal 1 - W2E Worker**:
```bash
cd apps/w2e
python manage.py runw2eworker
```

**Terminal 2 - EMB Worker**:
```bash
cd apps/emb
python manage.py runembworker
```

### 4. Trigger Workflow

**Terminal 3 - Web Workflow**:
```bash
cd apps/web
python manage.py run_workflow
```

---

## Expected Output

### Terminal 1 (W2E Worker):
```
Starting w2e worker on queue "w2e"...
Worker started...

[W2E -> EMB] Received sensitive data: first-emb-request
[W2E -> EMB] Return task ID: web-placeholder-task-123
[W2E -> EMB] De-sensitized data: second-emb-request
[W2E -> EMB] Enqueueing task to emb AI model
[W2E -> EMB] Enqueued to emb with ID: <task-id>

[W2E <- EMB] Received AI result: second-emb-result
[W2E <- EMB] Sending result back to web task: web-placeholder-task-123
[W2E <- EMB] Result delivered to web
```

### Terminal 2 (EMB Worker):
```
Starting emb worker on queue "emb"...
Worker started...

[AI Model] Received non-sensitive data: second-emb-request
[AI Model] Return task ID: web-placeholder-task-123
[AI Model] Returning result: second-emb-result
[AI Model] Enqueueing callback to bridge
```

### Terminal 3 (Web Workflow):
```
=== Starting Cross-Project Task Workflow ===

[Web] Sensitive data: first-emb-request
[Web] Return task ID: web-placeholder-task-123
[Web] Enqueueing task to bridge...
[Web] Task enqueued with ID: <task-id>

[Web] Workflow initiated successfully!

Note: This is an async workflow.
Check worker logs to see the full flow:
  1. Web -> Bridge (web_to_emb)
  2. Bridge -> AI Model (process_with_ai_model)
  3. AI Model -> Bridge (emb_to_web callback)
  4. Bridge -> Web (result delivery)
```

---

## Architecture Decisions

### 1. Why `foobar_*` Module Naming?

To match real-world project naming conventions where modules are prefixed with the project name to avoid collisions and improve clarity.

### 2. Why Centralized `core/settings.py`?

Separates configuration from application logic. The `core` module is not an app - it's purely for settings and management commands.

### 3. Why Two Redis Instances?

**Security isolation**: Sensitive data on redis-web should never be accessible to workers that process non-sensitive data on redis-emb. This physical separation enforces security boundaries.

### 4. Why Async Callbacks Instead of Polling?

**Polling doesn't work across Redis backends**:
```python
# This fails when task is on different Redis:
task_result = external_task.enqueue(data)
task_result.refresh()  # ❌ ConnectionError or stale data
```

**Callbacks work everywhere**:
```python
# Callback is just another task enqueue - always works:
def my_task(data, callback_id):
    result = process(data)
    callback_task.enqueue(result, callback_id)  # ✅ Works across any backend
```

### 5. Why Custom Worker Commands?

Developer experience. Compare:

**Without custom command**:
```bash
python manage.py rqworker w2e --job-class django_tasks.backends.rq.Job --with-scheduler
```

**With custom command**:
```bash
python manage.py runw2eworker
```

Much simpler, less error-prone, and self-documenting.

### 6. Why Dummy Task Stubs?

Enables **type-safe cross-project task enqueueing**:
- IDE autocomplete works
- Type checkers can validate parameters
- Runtime safety (NotImplementedError if accidentally called directly)
- Clear separation: stub = enqueue only, implementation = execution only

---

## Key Files Reference

| File | Purpose |
|------|---------|
| [`apps/web/foobar_web/management/commands/run_workflow.py`](apps/web/foobar_web/management/commands/run_workflow.py) | Workflow initiation |
| [`apps/web/foobar_w2e/tasks.py`](apps/web/foobar_w2e/tasks.py) | Dummy stubs for w2e tasks |
| [`apps/w2e/core/settings.py`](apps/w2e/core/settings.py) | Multi-backend configuration |
| [`apps/w2e/core/management/commands/runw2eworker.py`](apps/w2e/core/management/commands/runw2eworker.py) | Custom worker command |
| [`apps/w2e/foobar_w2e/tasks.py`](apps/w2e/foobar_w2e/tasks.py) | W2E task implementations |
| [`apps/w2e/foobar_emb/tasks.py`](apps/w2e/foobar_emb/tasks.py) | Dummy stubs for emb tasks |
| [`apps/emb/core/management/commands/runembworker.py`](apps/emb/core/management/commands/runembworker.py) | Custom worker command |
| [`apps/emb/foobar_emb/tasks.py`](apps/emb/foobar_emb/tasks.py) | EMB task implementation |
| [`apps/emb/foobar_w2e/tasks.py`](apps/emb/foobar_w2e/tasks.py) | Dummy stubs for w2e callbacks |

---

## Troubleshooting

### Redis Connection Errors

**Error**: `ConnectionError: Error 111 connecting to localhost:6379`

**Solution**: Ensure Redis services are running:
```bash
docker-compose ps
docker-compose up -d  # Start if not running
```

### Tasks Not Processing

**Check worker logs**: Ensure both workers are running and connected to correct Redis instances.

**Verify queue names**: Task `queue_name` must match worker queue argument.

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'foobar_w2e'`

**Solution**: Ensure module is in `INSTALLED_APPS` in settings:
```python
INSTALLED_APPS = [
    'foobar_web',
    'foobar_w2e',
    'foobar_emb',
]
```

---

## License

MIT
