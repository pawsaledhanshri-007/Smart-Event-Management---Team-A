# DATABASE.md — Smart Event Management System

**Author / Maintainer:** Alisha
**License:** © 2026 Alisha. All rights reserved. This documentation and the accompanying database schema may not be reproduced or distributed without permission from the author.

---

## 1. Database Overview

The Smart Event Management System uses PostgreSQL as its primary relational database.

The database layer is responsible for:

- PostgreSQL database setup
- Database schema design
- SQLAlchemy ORM models
- Relationships and foreign keys
- Constraints and indexes
- Registration and event business logic
- Alembic migrations
- Seed data
- pgvector support for RAG/embeddings

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL 17 | Primary relational database |
| SQLAlchemy 2.x | ORM and database interaction |
| psycopg 3 | PostgreSQL driver |
| Alembic | Database migrations |
| pgvector | Vector storage for RAG |
| Python 3.12+ | Backend/database services |
| python-dotenv | Environment variable management |

---

## 3. Setup & Environment

### PostgreSQL Configuration

```text
Database: event_management
User: event_admin
Host: localhost
Port: 5432
```

The database connection is configured using the `DATABASE_URL` environment variable.

```env
DATABASE_URL=postgresql+psycopg://event_admin:YOUR_PASSWORD@localhost:5432/event_management
```

The actual `.env` file contains the real database password and must not be committed to Git. Developers should use `.env.example` as a template.

### PostgreSQL Extensions

`pgcrypto` is used for UUID generation:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

`pgvector` is used for embedding storage:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Vector embeddings are stored using:

```text
VECTOR(1536)
```

---

## 4. Database Schema

The database contains 10 tables.

### 4.1 users

Stores application users and their roles.

| Column | Description |
|---|---|
| id | UUID primary key |
| name | User name |
| email | Unique email address |
| phone | Optional phone number |
| age | Optional age |
| college | Optional college |
| password_hash | Hashed password |
| role | User role |
| is_active | Account active status |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

Allowed roles: `admin`, `organizer`, `participant`

Constraints:
- Email must be unique.
- Role must be one of the allowed values.
- Age must be valid when provided.

---

### 4.2 venues

Stores event venues.

| Column | Description |
|---|---|
| id | UUID primary key |
| name | Venue name |
| location | Venue location |
| capacity | Maximum venue capacity |
| created_at | Creation timestamp |

Constraint: `capacity > 0`

---

### 4.3 events

Stores events created by organizers.

| Column | Description |
|---|---|
| id | UUID primary key |
| title | Event title |
| description | Event description |
| venue_id | Associated venue |
| organizer_id | Event organizer |
| start_time | Event start time |
| end_time | Event end time |
| capacity | Maximum event capacity |
| status | Event status |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

Allowed statuses: `scheduled`, `ongoing`, `completed`, `cancelled`

Constraints:
```text
end_time > start_time
capacity > 0
```

Foreign keys:
```text
venue_id → venues.id
organizer_id → users.id
```

---

### 4.4 registrations

Stores users registered for events.

| Column | Description |
|---|---|
| id | UUID primary key |
| user_id | Registered user |
| event_id | Registered event |
| status | Registration status |
| registered_at | Registration timestamp |
| cancelled_at | Cancellation timestamp |

Allowed statuses: `confirmed`, `cancelled`, `waitlisted`

A user cannot have duplicate registrations for the same event.

Unique constraint: `(user_id, event_id)`

Foreign keys:
```text
user_id → users.id
event_id → events.id
```

---

### 4.5 agent_sessions

Stores AI assistant sessions for users.

| Column | Description |
|---|---|
| id | UUID primary key |
| user_id | Associated user |
| started_at | Session start time |
| ended_at | Session end time |

Relationship: `users → agent_sessions`

---

### 4.6 agent_runs

Stores individual AI agent executions.

| Column | Description |
|---|---|
| id | UUID primary key |
| session_id | Related agent session |
| user_message | User message |
| intent | Detected intent |
| final_response | Agent response |
| latency_ms | Execution latency |
| created_at | Creation timestamp |

Constraint: latency value cannot be negative (`latency_ms >= 0`)

Foreign key: `session_id → agent_sessions.id`

---

### 4.7 tool_calls

Stores individual tool executions performed during an agent run.

| Column | Description |
|---|---|
| id | UUID primary key |
| run_id | Related agent run |
| tool_name | Name of the tool |
| tool_input | Tool input in JSON format |
| tool_output | Tool output in JSON format |
| error | Error information |
| latency_ms | Tool execution latency |
| created_at | Tool execution timestamp |

Constraint: latency value cannot be negative (`latency_ms >= 0`)

Foreign key: `run_id → agent_runs.id`

---

### 4.8 knowledge_documents

Stores document-level information used by the knowledge/RAG system.

| Column | Description |
|---|---|
| id | UUID primary key |
| title | Document title |
| source_path | Source document path |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

---

### 4.9 knowledge_chunks

Stores individual document chunks and their vector embeddings.

| Column | Description |
|---|---|
| id | UUID primary key |
| document_id | Related document |
| chunk_index | Position of the chunk |
| content | Chunk text |
| embedding | Vector embedding |

Embedding column type: `VECTOR(1536)`

Unique constraint: `(document_id, chunk_index)`

Foreign key: `document_id → knowledge_documents.id`

The actual document ingestion and embedding-generation workflow is implemented on the Agent/RAG side.

---

### 4.10 audit_logs

Stores important application actions for traceability.

| Column | Description |
|---|---|
| id | UUID primary key |
| actor_id | User who performed the action |
| action | Action performed |
| entity_type | Type of affected entity |
| entity_id | ID of affected entity |
| details | Additional JSON information |
| created_at | Action timestamp |

Foreign key: `actor_id → users.id`

`actor_id` becomes `NULL` if the associated user is deleted.

---

## 5. Relationships & Foreign Keys

```text
users
  │
  ├──< events
  ├──< registrations
  ├──< agent_sessions
  └──< audit_logs

venues
  │
  └──< events

events
  │
  └──< registrations

agent_sessions
  │
  └──< agent_runs
          │
          └──< tool_calls

knowledge_documents
  │
  └──< knowledge_chunks
```

### Foreign Key Delete Rules

| Relationship | Delete Behavior |
|---|---|
| events → users | RESTRICT |
| events → venues | RESTRICT |
| registrations → users | CASCADE |
| registrations → events | CASCADE |
| agent_sessions → users | CASCADE |
| agent_runs → agent_sessions | CASCADE |
| tool_calls → agent_runs | CASCADE |
| knowledge_chunks → knowledge_documents | CASCADE |
| audit_logs → users | SET NULL |

---

## 6. Constraints & Indexes

### Constraints Summary

**Users**
```text
Unique email
Valid role
Valid age
```

**Venues**
```text
capacity > 0
```

**Events**
```text
end_time > start_time
capacity > 0
Valid status
```

**Registrations**
```text
Unique(user_id, event_id)
Valid registration status
```

**Agent Runs**
```text
latency_ms >= 0
```

**Tool Calls**
```text
latency_ms >= 0
```

**Knowledge Chunks**
```text
Unique(document_id, chunk_index)
```

### Important Indexes

```text
events.venue_id
events.organizer_id
events.start_time

registrations.user_id
registrations.event_id

agent_sessions.user_id

agent_runs.session_id
agent_runs.created_at

tool_calls.run_id
tool_calls.tool_name

knowledge_chunks.document_id

audit_logs.actor_id
audit_logs.created_at
```

---

## 7. SQLAlchemy Models

SQLAlchemy models are located in:

```text
backend/app/models/
```

Structure:

```text
backend/app/models/
├── __init__.py
├── base.py
├── user.py
├── venue.py
├── event.py
├── registration.py
├── agent_session.py
├── agent_run.py
├── tool_call.py
├── knowledge.py
└── audit_log.py
```

Import pattern:

```python
from app.models import (
    User,
    Venue,
    Event,
    Registration,
    AgentSession,
    AgentRun,
    ToolCall,
    KnowledgeDocument,
    KnowledgeChunk,
    AuditLog,
)
```

The backend should reuse these models instead of creating duplicate models.

---

## 8. Database Session

Database connection and session management are handled by:

```text
backend/app/db/session.py
```

The session uses SQLAlchemy's `SessionLocal`.

```python
from app.db.session import SessionLocal

db = SessionLocal()

try:
    # database operations
    pass
finally:
    db.close()
```

The database URL is loaded from `.env`.

---

## 9. Services

Database-related business services are located in:

```text
backend/app/services/
```

Current services:

```text
registration_service.py
event_service.py
venue_service.py
```

### 9.1 Registration

```python
register_user_for_event(
    db,
    user_id,
    event_id
)
```

The registration service checks:

1. User exists and is active.
2. Event exists.
3. Event status is `scheduled`.
4. User is not already registered.
5. Event capacity has not been reached.
6. Registration is created with status `confirmed`.

```python
from app.services.registration_service import register_user_for_event

registration = register_user_for_event(
    db,
    user_id,
    event_id
)
```

If a business rule is violated, the service raises `ValueError`.

---

### 9.2 Cancellation

```python
cancel_registration(
    db,
    user_id,
    event_id
)
```

Cancellation changes the registration status:

```text
confirmed → cancelled
```

The `cancelled_at` timestamp is also recorded. The registration row is not deleted so that registration history can be preserved.

---

### 9.3 Event

Event creation logic is located at:

```text
backend/app/services/event_service.py
```

```python
create_event(...)
```

The service checks:

- Venue exists.
- End time is after start time.
- Event capacity is greater than zero.
- Event capacity does not exceed venue capacity.

---

### 9.4 Venue

Venue-related logic is located at:

```text
backend/app/services/venue_service.py
```

```python
get_venue_available_events(...)
check_venue_available(...)
```

The availability check detects overlapping events at the same venue.

Overlap condition:

```python
existing_event.start_time < requested_end_time
and
existing_event.end_time > requested_start_time
```

---

## 10. Alembic / Migrations

Alembic is used to manage database schema migrations.

Location:

```text
backend/alembic/
```

Configuration:

```text
backend/alembic.ini
```

The project database existed before Alembic was introduced. Therefore, a baseline migration was created instead of recreating the existing tables.

Current baseline revision:

```text
7c7bf3ebec9d
```

### Check Current Migration

Run from the `backend` directory:

```powershell
alembic current
```

Expected:

```text
7c7bf3ebec9d (head)
```

### Check Model/Database Synchronization

```powershell
alembic check
```

Expected:

```text
No new upgrade operations detected.
```

Future database schema changes should be handled using Alembic migrations. Do not create a new initial migration for the existing database.

---

## 11. Seed Data

Sample development data is provided by:

```text
backend/seed_data.py
```

The seed script creates sample:

- Users
- Venues
- Events
- Registrations

The seed data is intended for local development and testing.

---

## 12. File Structure

The relevant database files are:

```text
Smart-Event-Management---Team-A/
│
├── .env.example
├── .gitignore
├── DATABASE.md
├── schema.sql
│
└── backend/
    │
    ├── alembic/
    │   ├── versions/
    │   │   └── 7c7bf3ebec9d_baseline_existing_database.py
    │   ├── env.py
    │   └── script.py.mako
    │
    ├── alembic.ini
    │
    ├── app/
    │   │
    │   ├── db/
    │   │   ├── __init__.py
    │   │   └── session.py
    │   │
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── user.py
    │   │   ├── venue.py
    │   │   ├── event.py
    │   │   ├── registration.py
    │   │   ├── agent_session.py
    │   │   ├── agent_run.py
    │   │   ├── tool_call.py
    │   │   ├── knowledge.py
    │   │   └── audit_log.py
    │   │
    │   └── services/
    │       ├── __init__.py
    │       ├── registration_service.py
    │       ├── event_service.py
    │       └── venue_service.py
    │
    └── seed_data.py
```
