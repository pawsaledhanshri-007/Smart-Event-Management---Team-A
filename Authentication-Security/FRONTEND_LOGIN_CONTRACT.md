# Frontend Login Contract

The uploaded ZIP does not contain a frontend folder. The backend is ready for a simple two-option login screen.

## UI

Show two account-type buttons or tabs:

- User
- Admin

Then show only:

- Email / ID
- Password
- Sign In button

Public signup creates only a User (`participant`). Do not provide Admin signup.

## Request

Send an `application/x-www-form-urlencoded` request to `POST /api/auth/login` with:

```text
username=user@example.com
password=the-password
role=user
```

For Admin login, send `role=admin`.

The backend rejects an Admin account when `role=user`, and rejects a User account when `role=admin`, even if the email and password are correct.

There is no Google-login or OTP endpoint in this uploaded version. Google Gemini references belong to the AI/RAG modules and are unrelated to authentication.
