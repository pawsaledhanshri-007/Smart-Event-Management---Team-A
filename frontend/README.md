# Evently Frontend — User/Admin Login

React + Vite frontend for the Evently Smart Event Management project.

## Authentication flow

- The login page has two explicit account types: **User** and **Admin**.
- It sends `username`, `password`, and `role` to `POST /api/auth/login` as form data.
- User credentials work only with the User option.
- Admin credentials work only with the Admin option.
- Public signup creates only a User account. Admin signup is intentionally disabled.
- Google, Clerk, OTP, email-verification, password-reset, 2FA, and Event Manager login screens were removed.

This frontend is designed for the matching Authentication & Security backend package.

## Run

```bash
cp .env.example .env
npm install
npm run dev
```

## Validate

```bash
npm run lint
npm run build
```
