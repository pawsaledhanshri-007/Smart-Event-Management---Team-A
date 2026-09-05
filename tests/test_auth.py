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
        "password": "testpassword123"
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
        "password": "testpassword123"
    }
    login_response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
