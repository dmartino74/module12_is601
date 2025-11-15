from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/users/register",
        json={"username": "testuser", "password": "secret123", "email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_login_user_success():
    # Register first
    client.post(
        "/users/register",
        json={"username": "loginuser", "password": "mypassword", "email": "login@example.com"}
    )
    response = client.post(
        "/users/login",
        json={"username": "loginuser", "password": "mypassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_fail():
    response = client.post(
        "/users/login",
        json={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 401
