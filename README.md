# Django Tasks Bridge Playground

This project demonstrates a cross-project Django Tasks workflow with a bridge pattern for handling sensitive data.

## Architecture

The system consists of three Django projects:

1. **web** (`apps/web/`) - Handles sensitive data and initiates workflows
2. **w2e** (`apps/w2e/`) - Web-to-Emb bridge that de-sensitizes data
3. **emb** (`apps/emb/`) - AI model that processes non-sensitive data

## Data Flow

```
[Web Project]
    |
    | (1) Enqueues "first-emb-request"
    |     to redis-web queue
    v
[W2E Bridge]
    |
    | (2) De-sensitizes to "second-emb-request"
    |     Enqueues to redis-emb queue
    v
[Emb AI Model]
    |
    | (3) Returns "second-emb-result"
    v
[W2E Bridge]
    |
    | (4) Returns result
    v
[Web Project]
    |
    | (5) Displays result to user
```

## Directory Structure

```
.
├── apps/
│   ├── web/              # Django project with sensitive data access
│   │   ├── web/          # Project settings
│   │   ├── core/         # Core app with management command
│   │   ├── manage.py
│   │   └── requirements.txt
│   ├── w2e/              # Web-to-Emb bridge project
│   │   ├── w2e/          # Project settings
│   │   ├── bridge/       # Bridge component (de-sensitization)
│   │   ├── manage.py
│   │   ├── run_worker.sh # Bridge worker script
│   │   ├── test_workflow.py
│   │   └── requirements.txt
│   └── emb/              # AI model project
│       ├── emb/          # Project settings
│       ├── aimodel/      # AI model component
│       ├── manage.py
│       ├── run_worker.sh # AI model worker script
│       └── requirements.txt
├── deps/                 # Dependencies data (gitignored)
│   ├── postgres/
│   ├── redis-web/
│   └── redis-emb/
└── docker-compose.yml    # Database and Redis services
```

## Minimal Django Configuration

All three projects use **minimal Django configurations** since they don't serve web pages:

**What's included:**
- `SECRET_KEY` - Required by Django
- `INSTALLED_APPS` - Only essential apps (contenttypes, django_tasks, task apps)
- `DATABASES` - Minimal database config (SQLite for testing, PostgreSQL for web in production)
- `TASKS` - Django Tasks backend configuration
- `DEFAULT_AUTO_FIELD` and `USE_TZ` - To suppress warnings

**What's removed:**
- No `MIDDLEWARE` - Not needed without HTTP requests
- No `ROOT_URLCONF`, `urls.py` - No URL routing
- No `WSGI_APPLICATION`, `wsgi.py` - No WSGI server
- No `TEMPLATES` - No template rendering
- No `ALLOWED_HOSTS` - No HTTP serving

This keeps the configuration minimal and focused on task processing only.

## Quick Testing (No Docker Required)

To test the workflow without setting up Docker/Redis:

```bash
cd apps/w2e
pip install -r requirements.txt
python manage.py migrate  # Creates local SQLite database
python test_workflow.py
```

This runs the complete workflow synchronously using the immediate backend, demonstrating:
- ✓ AI model task execution
- ✓ Bridge task de-sensitizing data
- ✓ Full workflow from sensitive input to final result

## Full Setup (Production Mode with Redis)

### 1. Start Dependencies

Start PostgreSQL and Redis services:

```bash
docker-compose up -d
```

Verify services are running:

```bash
docker-compose ps
```

### 2. Install Python Dependencies

For the web project:

```bash
cd apps/web
pip install -r requirements.txt
```

For the w2e bridge project:

```bash
cd apps/w2e
pip install -r requirements.txt
```

For the emb AI model project:

```bash
cd apps/emb
pip install -r requirements.txt
```

### 3. Run Migrations

For web project with PostgreSQL:

```bash
cd apps/web
USE_POSTGRES=1 python manage.py migrate
```

For w2e bridge project with SQLite:

```bash
cd apps/w2e
python manage.py migrate
```

For emb AI model project with SQLite:

```bash
cd apps/emb
python manage.py migrate
```

## Running the Production Workflow (With Redis)

You need three terminal windows to run the complete workflow with Redis:

### Terminal 1: W2E Bridge Worker

```bash
cd apps/w2e
USE_REDIS=1 ./run_worker.sh
```

This worker listens to `redis-web` (port 6379) for tasks from the web project.

### Terminal 2: Emb AI Model Worker

```bash
cd apps/emb
USE_REDIS=1 ./run_worker.sh
```

This worker listens to `redis-emb` (port 6380) for tasks from the w2e bridge.

### Terminal 3: Trigger Workflow

```bash
cd apps/web
USE_REDIS=1 python manage.py run_workflow
```

This command will:
1. Enqueue a task to the bridge with sensitive data
2. Wait for the result
3. Display the final output

## Expected Output

When you run the workflow, you should see:

**Terminal 1 (Bridge Worker):**
```
[Bridge] Received sensitive data: first-emb-request
[Bridge] De-sensitized data: second-emb-request
[Bridge] Enqueueing task to AI model component
[Bridge] Received result from AI model: second-emb-result
```

**Terminal 2 (AI Model Worker):**
```
[AI Model] Received non-sensitive data: second-emb-request
[AI Model] Returning result: second-emb-result
```

**Terminal 3 (Web Command):**
```
=== Starting Cross-Project Task Workflow ===

[Web] Enqueueing task to bridge with data: first-emb-request
[Web] Task enqueued with ID: <task-id>
[Web] Waiting for result...

[Web] Received final result: second-emb-result

=== Workflow Complete ===
```

## Task Backends

The project uses multiple Redis backends for task queues:

- **redis-web** (localhost:6379) - Shared between web and bridge
- **redis-emb** (localhost:6380) - Used by bridge and AI model for internal tasks

## Cleaning Up

Stop all services:

```bash
docker-compose down
```

To remove all data volumes:

```bash
docker-compose down -v
rm -rf deps/postgres/ deps/redis-web/ deps/redis-emb/
```

## Development Notes

- The web project uses PostgreSQL for its database
- The emb project uses SQLite (no database needed for this demo)
- All task inputs/outputs are hardcoded as specified:
  - Input to bridge: `"first-emb-request"`
  - Input to AI model: `"second-emb-request"`
  - Output from AI model: `"second-emb-result"`

## Troubleshooting

### Workers not processing tasks

Make sure all three services are running:
```bash
docker-compose ps
```

All should show status "Up".

### Connection refused errors

Wait a few seconds for Redis and PostgreSQL to fully start:
```bash
docker-compose logs redis-web redis-emb postgres
```

### Task timeout

If the workflow times out:
1. Verify both workers are running
2. Check worker logs for errors
3. Verify Redis services are accessible

### Port conflicts

If ports 5432, 6379, or 6380 are already in use, update `docker-compose.yml` to use different ports.
