import pytest
from app.core.config import settings
from app.models.user import User, UserRole
from app.core import security

def test_register_user(client):
    data = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["email"] == data["email"]
    assert "id" in content

def test_login_user(client):
    data = {
        "username": "testuser@example.com",
        "password": "testpassword123",
        "role": "user",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content

def test_read_me(client, db):
    # Ensure user exists (might be carried over from previous tests depending on execution order, but conftest uses module scope)
    # Get token
    data = {
        "username": "testuser@example.com",
        "password": "testpassword123",
        "role": "user",
    }
    login_response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_admin_and_user_role_isolation(client, db):
    admin = User(
        email="admin@example.com",
        name="Test Admin",
        password_hash=security.get_password_hash("AdminPassword123!"),
        role=UserRole.ADMIN.value,
        is_active=True,
    )
    db.add(admin)
    db.commit()

    admin_as_user = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "admin@example.com",
            "password": "AdminPassword123!",
            "role": "user",
        },
    )
    assert admin_as_user.status_code == 401

    user_as_admin = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "testpassword123",
            "role": "admin",
        },
    )
    assert user_as_admin.status_code == 401

    correct_admin = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "admin@example.com",
            "password": "AdminPassword123!",
            "role": "admin",
        },
    )
    assert correct_admin.status_code == 200
