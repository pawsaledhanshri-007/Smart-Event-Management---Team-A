import time
from datetime import timedelta

from app.core import security
from app.core.config import settings
from app.models.user import User


def _register(client, email="testuser@example.com", password="testpassword123"):
    return client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": email, "name": "Test User", "password": password},
    )


def _login(client, email="testuser@example.com", password="testpassword123"):
    return client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": email, "password": password},
    )


def test_register_login_refresh_logout_and_me(client):
    response = _register(client)
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["is_email_verified"] is False

    login = _login(client)
    assert login.status_code == 200
    data = login.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["two_factor_required"] is False

    me = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == "testuser@example.com"

    refreshed = client.post(
        f"{settings.API_V1_STR}/auth/refresh",
        json={"refresh_token": data["refresh_token"]},
    )
    assert refreshed.status_code == 200
    refreshed_data = refreshed.json()
    assert refreshed_data["access_token"]
    assert refreshed_data["refresh_token"] != data["refresh_token"]

    logout = client.post(
        f"{settings.API_V1_STR}/auth/logout",
        json={"refresh_token": refreshed_data["refresh_token"]},
    )
    assert logout.status_code == 200

    revoked_me = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {refreshed_data['access_token']}"},
    )
    assert revoked_me.status_code == 401


def test_email_verification_reset_and_change_password(client, db):
    email = "security@example.com"
    old_password = "OldPassword123"
    new_password = "NewPassword123"
    final_password = "FinalPassword123"

    assert _register(client, email, old_password).status_code == 201
    user = db.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.is_email_verified is False

    verification_token = security.create_purpose_token(
        subject=user.id,
        purpose="email_verification",
        expires_delta=timedelta(minutes=10),
        extra_claims={"email": user.email},
    )
    verified = client.post(
        f"{settings.API_V1_STR}/auth/verify-email",
        json={"token": verification_token},
    )
    assert verified.status_code == 200
    db.refresh(user)
    assert user.is_email_verified is True

    reset_token = security.create_purpose_token(
        subject=user.id,
        purpose="password_reset",
        expires_delta=timedelta(minutes=10),
        extra_claims={"ver": user.password_reset_version},
    )
    reset = client.post(
        f"{settings.API_V1_STR}/auth/reset-password",
        json={"token": reset_token, "new_password": new_password},
    )
    assert reset.status_code == 200
    assert _login(client, email, old_password).status_code == 401

    login = _login(client, email, new_password)
    assert login.status_code == 200
    token = login.json()["access_token"]

    changed = client.post(
        f"{settings.API_V1_STR}/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": new_password, "new_password": final_password},
    )
    assert changed.status_code == 200

    # Change-password revokes all active sessions.
    old_session = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert old_session.status_code == 401
    assert _login(client, email, final_password).status_code == 200


def test_totp_two_factor_login(client):
    email = "mfa@example.com"
    password = "MfaPassword123"
    assert _register(client, email, password).status_code == 201

    login = _login(client, email, password)
    access_token = login.json()["access_token"]

    setup = client.post(
        f"{settings.API_V1_STR}/auth/2fa/setup",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert setup.status_code == 200
    secret = setup.json()["secret"]
    code = security._totp_code(secret, int(time.time()))

    enabled = client.post(
        f"{settings.API_V1_STR}/auth/2fa/enable",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"code": code},
    )
    assert enabled.status_code == 200

    challenged = _login(client, email, password)
    assert challenged.status_code == 200
    challenge_data = challenged.json()
    assert challenge_data["two_factor_required"] is True
    assert challenge_data["access_token"] is None

    code = security._totp_code(secret, int(time.time()))
    verified = client.post(
        f"{settings.API_V1_STR}/auth/2fa/verify-login",
        json={
            "challenge_token": challenge_data["challenge_token"],
            "code": code,
        },
    )
    assert verified.status_code == 200
    assert verified.json()["access_token"]
    assert verified.json()["refresh_token"]
