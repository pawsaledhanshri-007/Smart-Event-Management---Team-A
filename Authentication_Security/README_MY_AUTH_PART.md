# Authentication & Security — Previous Work + New Selected Features

This folder keeps the previously completed Authentication & Security files and attaches the new work selected for the next phase.

## Previously completed

- Registration
- Email/password login
- Google Sign-In backend
- JWT authentication
- `/api/auth/me`
- RBAC dependencies for admin / organizer / participant
- bcrypt password hashing

## Newly added now

1. Forgot Password
2. Reset Password
3. Change Password
4. Normal Email Verification
5. Refresh Token
6. Token Revocation / Better Logout
10. Optional TOTP 2FA/MFA

Read `README_AUTH_SECURITY_EXTENSIONS.md` for endpoints, configuration and database-upgrade instructions.

This is an auth-focused study/merge package. The full integrated project ZIP is provided separately because these files depend on shared project files such as `db/session.py`, `models/base.py`, API router setup, PostgreSQL and the frontend.
