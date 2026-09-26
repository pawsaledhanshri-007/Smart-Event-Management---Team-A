# Evently Authentication & Security Role

Contains bcrypt password hashing, signed HS256 JWT login, protected-user dependencies, strict Admin/User account-type isolation, user registration, secure environment-based Admin seeding, and authentication tests.

Public signup creates only a User. Admin credentials must be configured in the root `.env`, then created through `backend/seed_data.py`.

This is a role handoff intended to be merged into the complete team repository. Read `FRONTEND_LOGIN_CONTRACT.md` for the exact frontend request format.
