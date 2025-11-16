import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient instance once for all tests
client = TestClient(app)


def test_homepage_loads():
    """Check that the homepage returns the expected JSON payload"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Calculator API"
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"


def test_register_user():
    """Register a new user successfully with unique credentials"""
    unique_name = f"e2euser_{uuid.uuid4().hex[:6]}"
    unique_email = f"{unique_name}@example.com"
    response = client.post(
        "/users/register",
        json={
            "username": unique_name,
            "password": "SecurePass123!",
            "email": unique_email
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == unique_name
    assert data["email"] == unique_email


def test_login_user_success():
    """Login with correct credentials"""
    # First register
    client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "password": "SecurePass123!",
            "email": "login@example.com"
        }
    )
    # Then login
    response = client.post(
        "/users/login",
        json={
            "username": "loginuser",
            "password": "SecurePass123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["username"] == "loginuser"


def test_login_user_fail():
    """Login fails with wrong password"""
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "failuser",
            "password": "SecurePass123!",
            "email": "fail@example.com"
        }
    )
    # Attempt login with wrong password
    response = client.post(
        "/users/login",
        json={
            "username": "failuser",
            "password": "WrongPass!"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_register_duplicate_username():
    """Duplicate usernames are rejected"""
    client.post(
        "/users/register",
        json={
            "username": "dupuser",
            "password": "SecurePass123!",
            "email": "dup1@example.com"
        }
    )
    response = client.post(
        "/users/register",
        json={
            "username": "dupuser",
            "password": "SecurePass123!",
            "email": "dup2@example.com"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_password_too_long():
    """Passwords longer than 72 bytes are rejected"""
    long_pw = "a" * 100  # >72 bytes
    response = client.post(
        "/users/register",
        json={
            "username": "toolonguser",
            "password": long_pw,
            "email": "toolong@example.com"
        }
    )
    # Depending on schema vs route validation:
    assert response.status_code in (400, 422)
    if response.status_code == 400:
        assert response.json()["detail"] == "Password too long (max 72 bytes)"
    elif response.status_code == 422:
        # Pydantic validation error
        assert "password" in str(response.json())
