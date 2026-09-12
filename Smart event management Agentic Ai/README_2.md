# README 2 — Authentication Integration Notes

This file combines the extra integration/check documentation that was previously
stored in multiple separate files. The original `README.md` is kept unchanged.

---

## 1. Authentication Integration

This folder is built from the team's `integration/final-structure` layout and
places Authentication directly inside the real FastAPI backend package.

## Where Authentication is now connected

- `backend/app/api/auth.py`
  - registration
  - login
  - `/me`
- `backend/app/api/deps.py`
  - JWT validation
  - current-user identity
  - inactive-user rejection
  - admin role dependency
- `backend/app/core/security.py`
  - bcrypt hashing
  - password verification
  - JWT creation
- `backend/app/models/user.py`
  - uses the integrated UUID database model
  - roles remain database-compatible: `admin`, `organizer`, `participant`
- `backend/app/api/events.py`
- `backend/app/api/venues.py`
- `backend/app/api/registrations.py`
  - only minimal Authentication/RBAC dependency wiring was added.

## API paths

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

Login uses form data:
- `username` = email
- `password` = password

Protected requests use:
`Authorization: Bearer <JWT>`

## Important integration choice

The current integrated database accepts:
- `admin`
- `organizer`
- `participant`

Therefore this merged package does NOT force the older standalone
`USER` / `ADMIN` uppercase values, because that would violate the current
database CHECK constraint.

New registration creates a `participant`.
Admin checks require role `admin`.

## Database compatibility

The integrated SQLAlchemy User model and seed data contain:
`phone`, `age`, `college`.

The root `schema.sql` currently does not contain those fields.

The original schema was preserved. An integration-only helper is included:

`integration_db_compat.sql`

Use it only when those columns are missing from the actual database.

## Dependency compatibility

The integrated knowledge model imports `pgvector.sqlalchemy`, while the
original `requirements.txt` does not include the Python pgvector package.

The original requirements file is preserved. For this merged package use:

`pip install -r requirements-integration.txt`

## Run location

Run FastAPI from the `backend` directory so `app` resolves correctly:

`uvicorn app.main:app --reload`

## Scope

This merge integrates Authentication into the team's existing structure.
It does not silently rewrite the Backend/Database business-service design.
See `KNOWN_EXISTING_INTEGRATION_ISSUES.md` for issues detected in the
existing integrated branch that are outside Authentication.

---

## 2. Existing Integration Issues

These were found in the team's existing `integration/final-structure`.
They are NOT Authentication logic errors.

1. `events.py` calls:
   - `event_service.get_all_events`
   - `event_service.get_event_by_id`
   - `event_service.update_event`
   - `event_service.delete_event`
   but the current `event_service.py` only defines `create_event`, and its
   current function signature also does not match the API call.

2. `venues.py` calls CRUD functions such as:
   - `get_all_venues`
   - `get_venue_by_id`
   - `create_venue`
   - `update_venue`
   - `delete_venue`
   but the current `venue_service.py` only contains venue-availability helpers.

3. `registrations.py` calls:
   - `get_registrations_by_event`
   - `get_registrations_by_user`
   but those functions are not currently present in `registration_service.py`.

4. The original root `schema.sql` lacks `phone`, `age`, `college`, while the
   integrated User model and seed data expect them. This package includes an
   integration-only SQL compatibility patch without replacing the original schema.

5. The existing knowledge model imports `pgvector.sqlalchemy`, but the original
   requirements file does not list the Python `pgvector` package. This package
   keeps the original file and adds `requirements-integration.txt`.

These points should be handled by the Backend / Database / Integration owner.
Authentication files are already adapted to the existing UUID user model,
database session, role values and API prefix.

---

## 3. Original Branch File Check

```text
COMPLETE INTEGRATION FILE CHECK
================================
Original integration/final-structure file paths checked: 54
Missing original paths: 0

[OK] .env.example
[OK] .gitignore
[OK] DATABASE.md
[OK] Dockerfile
[OK] LICENSE
[OK] README.md
[OK] docker-compose.yml
[OK] requirements.txt
[OK] schema.sql
[OK] backend/alembic.ini
[OK] backend/alembic/README
[OK] backend/alembic/env.py
[OK] backend/alembic/script.py.mako
[OK] backend/alembic/versions/7c7bf3ebec9d_baseline_existing_database.py
[OK] backend/app/__init__.py
[OK] backend/app/api/__init__.py
[OK] backend/app/api/auth.py
[OK] backend/app/api/deps.py
[OK] backend/app/api/events.py
[OK] backend/app/api/registrations.py
[OK] backend/app/api/venues.py
[OK] backend/app/core/config.py
[OK] backend/app/core/security.py
[OK] backend/app/db/__init__.py
[OK] backend/app/db/session.py
[OK] backend/app/main.py
[OK] backend/app/models/__init__.py
[OK] backend/app/models/agent_run.py
[OK] backend/app/models/agent_session.py
[OK] backend/app/models/audit_log.py
[OK] backend/app/models/base.py
[OK] backend/app/models/event.py
[OK] backend/app/models/knowledge.py
[OK] backend/app/models/registration.py
[OK] backend/app/models/tool_call.py
[OK] backend/app/models/user.py
[OK] backend/app/models/venue.py
[OK] backend/app/repositories/event_repository.py
[OK] backend/app/repositories/venue_repository.py
[OK] backend/app/schemas/event.py
[OK] backend/app/schemas/registration.py
[OK] backend/app/schemas/token.py
[OK] backend/app/schemas/user.py
[OK] backend/app/schemas/venue.py
[OK] backend/app/services/__init__.py
[OK] backend/app/services/event_service.py
[OK] backend/app/services/registration_service.py
[OK] backend/app/services/venue_service.py
[OK] backend/seed_data.py
[OK] backend/test_registration_service.py
[OK] tests/__init__.py
[OK] tests/conftest.py
[OK] tests/test_auth.py
[OK] tests/test_domain.py
```

---

## 4. Final File Map

```text
.env.example
.gitignore
COMPLETE_BRANCH_FILE_CHECK.txt
DATABASE.md
Dockerfile
FILE_MAP.txt
KNOWN_EXISTING_INTEGRATION_ISSUES.md
LICENSE
README.md
README_INTEGRATED_AUTH.md
backend/alembic.ini
backend/alembic/README
backend/alembic/env.py
backend/alembic/script.py.mako
backend/alembic/versions/7c7bf3ebec9d_baseline_existing_database.py
backend/app/__init__.py
backend/app/api/__init__.py
backend/app/api/auth.py
backend/app/api/deps.py
backend/app/api/events.py
backend/app/api/registrations.py
backend/app/api/venues.py
backend/app/core/config.py
backend/app/core/security.py
backend/app/db/__init__.py
backend/app/db/base.py
backend/app/db/session.py
backend/app/main.py
backend/app/models/__init__.py
backend/app/models/agent_run.py
backend/app/models/agent_session.py
backend/app/models/audit_log.py
backend/app/models/base.py
backend/app/models/event.py
backend/app/models/knowledge.py
backend/app/models/registration.py
backend/app/models/tool_call.py
backend/app/models/user.py
backend/app/models/venue.py
backend/app/repositories/event_repository.py
backend/app/repositories/venue_repository.py
backend/app/schemas/event.py
backend/app/schemas/registration.py
backend/app/schemas/token.py
backend/app/schemas/user.py
backend/app/schemas/venue.py
backend/app/services/__init__.py
backend/app/services/event_service.py
backend/app/services/registration_service.py
backend/app/services/venue_service.py
backend/seed_data.py
backend/test_registration_service.py
docker-compose.yml
integration_db_compat.sql
requirements-integration.txt
requirements.txt
schema.sql
tests/__init__.py
tests/conftest.py
tests/test_auth.py
tests/test_domain.py
```

---

## 5. Important Note

The Authentication code itself remains integrated inside the backend and was
not moved into this README file.

Core Authentication files remain:

- `backend/app/api/auth.py`
- `backend/app/api/deps.py`
- `backend/app/core/security.py`
- `backend/app/models/user.py`
- `backend/app/schemas/user.py`
- `backend/app/schemas/token.py`

The original project `README.md` remains separate. This `README_2.md` is only
for the Authentication integration and integration-check notes.

---

## 6. Google Sign-In Added to Authentication

Google Sign-In is now supported **alongside** the existing email/password login.
The frontend does not send the user's Gmail password to this backend.

### Backend endpoint

```text
POST /api/auth/google
```

Request body:

```json
{
  "credential": "GOOGLE_ID_TOKEN_FROM_FRONTEND"
}
```

Flow:

```text
Google Sign-In button on Frontend
        ↓
Google verifies the user's Google/Gmail account
        ↓
Frontend receives a Google ID token (credential)
        ↓
POST /api/auth/google
        ↓
security.py verifies the Google token and GOOGLE_CLIENT_ID
        ↓
auth.py checks the email in the existing users table
        ↓
Existing user → login
New user → create participant user
        ↓
Backend creates the project's normal JWT
        ↓
The same JWT works with /api/auth/me and protected backend APIs
```

### Files changed for Google authentication

- `backend/app/api/auth.py` — added `/google` login endpoint.
- `backend/app/core/security.py` — added Google ID-token verification.
- `backend/app/core/config.py` — added `GOOGLE_CLIENT_ID` setting.
- `backend/app/schemas/token.py` — added the Google credential request schema.
- `.env.example` — added the Google Client ID template.
- `requirements.txt` — added the `google-auth` Python dependency.

### Local setup later

Create a Google OAuth **Web application Client ID** and put it only in your local `.env`:

```env
GOOGLE_CLIENT_ID=xxxxxxxxxxxx-xxxxxxxxxxxxxxxx.apps.googleusercontent.com
```

The visual **Continue with Google** button belongs to the Frontend module. The
Authentication module's responsibility is to verify Google's credential, find
or create the user in PostgreSQL, and issue the application's JWT.
