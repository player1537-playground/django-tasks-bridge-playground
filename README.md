# Django Tasks Bridge Playground

This project demonstrates a cross-project Django Tasks workflow with a bridge pattern for handling sensitive data.

## Architecture

The system consists of two Django projects:

1. **web** (`apps/web/`) - Handles sensitive data and initiates workflows
2. **emb** (`apps/emb/`) - Contains two components:
   - **bridge** - De-sensitizes data and forwards to AI model
   - **aimodel** - Processes non-sensitive data through AI model

## Data Flow

```
[Web Project]
    |
    | (1) Enqueues "first-emb-request"
    |     to redis-web queue
    v
[Bridge Component]
    |
    | (2) De-sensitizes to "second-emb-request"
    |     Enqueues to redis-emb queue
    v
[AI Model Component]
    |
    | (3) Returns "second-emb-result"
    v
[Bridge Component]
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
│   │   └── manage.py
│   └── emb/              # Django project with bridge and AI model
│       ├── emb/          # Project settings
│       ├── bridge/       # Bridge component (de-sensitization)
│       ├── aimodel/      # AI model component
│       ├── manage.py
│       ├── run_bridge_worker.sh    # Bridge worker script
│       └── run_aimodel_worker.sh   # AI model worker script
├── deps/                 # Dependencies data (gitignored)
│   ├── postgres/
│   ├── redis-web/
│   └── redis-emb/
└── docker-compose.yml    # Database and Redis services
```

## Setup

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

For the emb project:

```bash
cd apps/emb
pip install -r requirements.txt
```

### 3. Run Migrations (Web Project Only)

The web project uses PostgreSQL:

```bash
cd apps/web
python manage.py migrate
```

## Running the Workflow

You need three terminal windows to run the complete workflow:

### Terminal 1: Bridge Worker

```bash
cd apps/emb
./run_bridge_worker.sh
```

This worker listens to `redis-web` (port 6379) for tasks from the web project.

### Terminal 2: AI Model Worker

```bash
cd apps/emb
./run_aimodel_worker.sh
```

This worker listens to `redis-emb` (port 6380) for tasks from the bridge component.

### Terminal 3: Trigger Workflow

```bash
cd apps/web
python manage.py run_workflow
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
