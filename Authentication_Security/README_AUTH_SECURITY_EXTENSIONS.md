# Authentication & Security — Added Features 1, 2, 3, 4, 5, 6 and 10

This package keeps the previously completed Authentication module and adds the seven features selected for the next phase.

## Added features

1. **Forgot Password** — `POST /api/auth/forgot-password`
2. **Reset Password** — `POST /api/auth/reset-password`
3. **Change Password** — `POST /api/auth/change-password`
4. **Normal Email Verification** — `POST /api/auth/resend-verification` and `POST /api/auth/verify-email`
5. **Refresh Token** — `POST /api/auth/refresh` with refresh-token rotation
6. **Token Revocation / Better Logout** — `POST /api/auth/logout` and `POST /api/auth/logout-all`; protected routes check server-side session revocation
10. **Optional 2FA/MFA** — TOTP authenticator flow using `/api/auth/2fa/setup`, `/enable`, `/disable`, and `/verify-login`

## New/updated backend files

- `backend/app/api/auth.py` — all auth endpoints
- `backend/app/api/deps.py` — JWT + revocable session check
- `backend/app/core/security.py` — access/refresh/action JWTs + TOTP
- `backend/app/core/config.py` — token, email, SMTP and 2FA settings
- `backend/app/models/user.py` — verification/reset/2FA fields
- `backend/app/models/auth_session.py` — refresh session/revocation table
- `backend/app/schemas/token.py`
- `backend/app/schemas/auth_security.py`
- `backend/app/services/auth_session_service.py`
- `backend/app/services/email_service.py`
- `backend/alembic/versions/9f3a2c1e6b7d_auth_security_extensions.py`
- `tests/test_auth.py`
- `.env.example`
- `schema.sql`

## Database upgrade

For an existing PostgreSQL database, run Alembic from the `backend` directory:

```bash
alembic upgrade head
```

For a fresh database, the updated `schema.sql` already contains the required fields and `auth_sessions` table.

## Email setup

Forgot-password and email verification support SMTP. Configure the `SMTP_*` values in the root `.env`.

For local development, `SMTP_HOST` can remain blank. The backend then writes the reset/verification link to its logs. You can temporarily set `AUTH_DEBUG_TOKENS=true` to return development tokens in the API response. Never enable this in production.

`REQUIRE_EMAIL_VERIFICATION=false` is the safe migration default, so old accounts can still sign in. After SMTP and the frontend verification page are ready, set it to `true` if verified email should be mandatory.

## Frontend still required

The backend APIs are implemented here. The frontend team still needs UI/pages for Forgot Password, Reset Password, Change Password, Verify Email, refresh-token storage/renewal, logout API use, and the 2FA code screen.
