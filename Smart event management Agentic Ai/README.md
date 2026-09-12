# Smart-Event-Management---Team-A
# Database Documentation — Smart Event Management System

**Author / Maintainer:** Alisha
**License:** © 2026 Alisha. All rights reserved. This documentation and the accompanying database schema may not be reproduced or distributed without permission from the author.

---

## 1. Overview

PostgreSQL-based database layer for the Smart Event Management System, covering schema design, SQLAlchemy ORM models, constraints/indexes, business logic services, Alembic migrations, seed data, and pgvector support for RAG.

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

```text
Database: event_management
User: event_admin
Host: localhost
Port: 5432
```

Connection string set via `DATABASE_URL` in `.env` (use `.env.example` as a template; never commit `.env`).

```env
DATABASE_URL=postgresql+psycopg://event_admin:YOUR_PASSWORD@localhost:5432/event_management
```

Required extensions:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- UUID generation
CREATE EXTENSION IF NOT EXISTS vector;    -- pgvector, VECTOR(1536) embeddings
```

---

## 4. Schema Summary (10 Tables)

| Table | Purpose | Key Constraints |
|---|---|---|
| **users** | App users & roles | Unique email; role ∈ {admin, organizer, participant}; valid age |
| **venues** | Event venues | capacity > 0 |
| **events** | Organizer-created events | end_time > start_time; capacity > 0; status ∈ {scheduled, ongoing, completed, cancelled}; FK → venues, users |
| **registrations** | User↔event registrations | Unique(user_id, event_id); status ∈ {confirmed, cancelled, waitlisted}; FK → users, events |
| **agent_sessions** | AI assistant sessions | FK → users |
| **agent_runs** | Individual agent executions | latency_ms ≥ 0; FK → agent_sessions |
| **tool_calls** | Tool executions within a run | latency_ms ≥ 0; FK → agent_runs |
| **knowledge_documents** | RAG document metadata | — |
| **knowledge_chunks** | Document chunks + embeddings | VECTOR(1536); Unique(document_id, chunk_index); FK → knowledge_documents |
| **audit_logs** | Action traceability | FK → users (nullable actor_id) |

Full column-level detail lives in `schema.sql` (validated against a live PostgreSQL instance).

---

## 5. Relationships

```text
users ──< events, registrations, agent_sessions, audit_logs
venues ──< events
events ──< registrations
agent_sessions ──< agent_runs ──< tool_calls
knowledge_documents ──< knowledge_chunks
```

### Delete Rules

| Relationship | Behavior |
|---|---|
| events → users / venues | RESTRICT |
| registrations → users / events | CASCADE |
| agent_sessions → users | CASCADE |
| agent_runs → agent_sessions | CASCADE |
| tool_calls → agent_runs | CASCADE |
| knowledge_chunks → knowledge_documents | CASCADE |
| audit_logs → users | SET NULL |

---

## 6. Key Indexes

```text
events: venue_id, organizer_id, start_time
registrations: user_id, event_id
agent_sessions: user_id
agent_runs: session_id, created_at
tool_calls: run_id, tool_name
knowledge_chunks: document_id
audit_logs: actor_id, created_at
```

---

## 7. SQLAlchemy Models

Located at `backend/app/models/`, importable via:

```python
from app.models import (
    User, Venue, Event, Registration,
    AgentSession, AgentRun, ToolCall,
    KnowledgeDocument, KnowledgeChunk, AuditLog,
)
```

Session management: `backend/app/db/session.py` (`SessionLocal`).

---

## 8. Services (`backend/app/services/`)

**Registration** — `register_user_for_event(db, user_id, event_id)`
Checks: user active → event exists → status is `scheduled` → not already registered → capacity available → creates `confirmed` registration. Raises `ValueError` on violation.

**Cancellation** — `cancel_registration(db, user_id, event_id)`
Sets status `confirmed → cancelled`, records `cancelled_at`. Row is preserved (not deleted).

**Event** — `create_event(...)` in `event_service.py`
Validates venue exists, end_time > start_time, capacity > 0, and capacity ≤ venue capacity.

**Venue** — `venue_service.py`
`get_venue_available_events(...)` and `check_venue_available(...)` detect overlapping bookings:

```python
existing.start_time < requested_end_time and existing.end_time > requested_start_time
```

---

## 9. Alembic Migrations

Location: `backend/alembic/`. Baseline revision (existing DB, no recreation): `7c7bf3ebec9d`.

```powershell
alembic current   # → 7c7bf3ebec9d (head)
alembic check     # → No new upgrade operations detected.
```

Future schema changes go through Alembic — do not create a new initial migration.

---

## 10. Seed Data

`backend/seed_data.py` populates sample users, venues, events, and registrations for local dev/testing.

---

## 11. File Structure

```text
Smart-Event-Management---Team-A/
├── .env.example
├── .gitignore
├── DATABASE.md
├── schema.sql
└── backend/
    ├── alembic/{versions/7c7bf3ebec9d_baseline_existing_database.py, env.py, script.py.mako}
    ├── alembic.ini
    ├── app/
    │   ├── db/session.py
    │   ├── models/{base,user,venue,event,registration,agent_session,agent_run,tool_call,knowledge,audit_log}.py
    │   └── services/{registration_service,event_service,venue_service}.py
    └── seed_data.py
```
