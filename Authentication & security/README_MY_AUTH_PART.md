# Authentication & Security — My Part Only

This folder contains only the files related to the Authentication & Security part
from the final integrated Smart Event Management project.

## Core files

1. `backend/app/api/auth.py`
   - User registration
   - Email/password login
   - Google/Gmail login
   - `/me` endpoint
   - Creates the application's JWT after successful login

2. `backend/app/api/deps.py`
   - Reads Bearer JWT from requests
   - Verifies JWT
   - Finds the current user
   - Rejects inactive/invalid users
   - Checks admin role

3. `backend/app/core/security.py`
   - Password hashing with bcrypt
   - Password verification
   - JWT creation
   - Google ID-token verification

4. `backend/app/core/config.py`
   - Authentication settings such as `SECRET_KEY`
   - JWT expiry time
   - `GOOGLE_CLIENT_ID`
   - Database URL is shared project configuration

5. `backend/app/models/user.py`
   - User account model used by Authentication
   - Defines user roles and account fields
   - This model is shared with the Database layer, but it is included here because
     Authentication reads and writes the `users` table through it.

6. `backend/app/schemas/user.py`
   - Defines registration input and user API response structure

7. `backend/app/schemas/token.py`
   - Defines JWT response payload
   - Defines decoded token payload
   - Defines Google credential request

8. `tests/test_auth.py`
   - Authentication API tests for register, login and `/me`

9. `.env.example`
   - Template for `SECRET_KEY`, JWT expiry, database URL and Google Client ID
   - Never put a real password or secret in GitHub

10. `requirements_auth.txt`
    - Dependencies used specifically by this Authentication & Security part

## Shared project files NOT included here

These are used by Authentication but belong to Backend/Database integration:

- `backend/app/db/session.py` → provides `get_db`
- `backend/app/models/base.py` → SQLAlchemy Base/TimestampMixin
- `backend/app/api/__init__.py` → mounts the auth router into the main API
- `backend/app/main.py` → starts the FastAPI app
- PostgreSQL database/schema → stores users
- Frontend Google button → obtains the Google credential and sends it to `/api/auth/google`

So this folder is for studying/presenting the Authentication & Security work only.
It is not a standalone copy of the whole application.
