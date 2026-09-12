import pytest
from app.core.config import settings
from app.models.user import User, UserRole
from app.core import security

@pytest.fixture
def admin_token(db, client):
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            name="Admin User",
            password_hash=security.get_password_hash("adminpassword"),
            role=UserRole.ADMIN
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    data = {"username": "admin@example.com", "password": "adminpassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    return response.json()["access_token"]

@pytest.fixture
def user_token(db, client):
    user = db.query(User).filter(User.email == "user@example.com").first()
    if not user:
        user = User(
            email="user@example.com",
            name="Normal User",
            password_hash=security.get_password_hash("userpassword"),
            role=UserRole.USER
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    data = {"username": "user@example.com", "password": "userpassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    return response.json()["access_token"]

def test_venue_creation_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {"name": "Main Hall", "capacity": 100, "location": "New York"}
    response = client.post(f"{settings.API_V1_STR}/venues/", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Main Hall"

def test_venue_creation_user(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"name": "Small Hall", "capacity": 50, "location": "New York"}
    response = client.post(f"{settings.API_V1_STR}/venues/", json=data, headers=headers)
    assert response.status_code == 403

def test_event_creation(client, admin_token, db):
    headers = {"Authorization": f"Bearer {admin_token}"}
    venue_response = client.post(
        f"{settings.API_V1_STR}/venues/",
        json={"name": "Event Hall", "capacity": 10, "location": "LA"},
        headers=headers
    )
    venue_id = venue_response.json()["id"]

    data = {
        "title": "Tech Conference",
        "description": "Annual tech conf",
        "date": "2027-10-10",
        "time": "09:00:00",
        "venue_id": venue_id,
        "capacity": 5
    }
    response = client.post(f"{settings.API_V1_STR}/events/", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Tech Conference"

def test_registration(client, user_token, admin_token):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    venue = client.post(
        f"{settings.API_V1_STR}/venues/",
        json={"name": "Reg Hall", "capacity": 5, "location": "SF"},
        headers=admin_headers
    ).json()

    event_data = {
        "title": "Reg Event",
        "date": "2027-11-11",
        "time": "10:00:00",
        "venue_id": venue["id"],
        "capacity": 1
    }
    event = client.post(
        f"{settings.API_V1_STR}/events/",
        json=event_data,
        headers=admin_headers
    ).json()

    response = client.post(
        f"{settings.API_V1_STR}/events/{event['id']}/register",
        headers=user_headers
    )
    assert response.status_code == 201
    assert response.json()["status"] == "REGISTERED"

    response_duplicate = client.post(
        f"{settings.API_V1_STR}/events/{event['id']}/register",
        headers=user_headers
    )
    assert response_duplicate.status_code == 409

    response_capacity = client.post(
        f"{settings.API_V1_STR}/events/{event['id']}/register",
        headers=admin_headers
    )
    assert response_capacity.status_code == 422

    response_cancel = client.delete(
        f"{settings.API_V1_STR}/events/{event['id']}/register",
        headers=user_headers
    )
    assert response_cancel.status_code == 204
