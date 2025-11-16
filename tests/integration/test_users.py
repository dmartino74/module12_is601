from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user(db_session):
    """Test user registration endpoint"""
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "password": "SecurePass123!",  # 15 chars - well within 72 limit
            "email": "test@example.com"
        }
    )
    
    assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "id" in data


def test_login_user_success(db_session):
    """Test successful user login"""
    # First register a user
    reg_response = client.post(
        "/users/register",
        json={
            "username": "logintest",
            "password": "SecurePass123!",
            "email": "login@example.com"
        }
    )
    assert reg_response.status_code == 200, f"Registration failed: {reg_response.text}"
    
    # Now try to login
    response = client.post(
        "/users/login",
        json={
            "username": "logintest",
            "password": "SecurePass123!"
        }
    )
    
    assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["username"] == "logintest"


def test_login_user_fail(db_session):
    """Test failed user login with wrong password"""
    # First register a user
    client.post(
        "/users/register",
        json={
            "username": "failtest",
            "password": "SecurePass123!",
            "email": "fail@example.com"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/users/login",
        json={
            "username": "failtest",
            "password": "WrongPass!"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid" in data["detail"]


def test_register_duplicate_username(db_session):
    """Test that duplicate usernames are rejected"""
    # Register first user
    client.post(
        "/users/register",
        json={
            "username": "duplicate",
            "password": "SecurePass123!",
            "email": "dup1@example.com"
        }
    )
    
    # Try to register same username again
    response = client.post(
        "/users/register",
        json={
            "username": "duplicate",
            "password": "SecurePass123!",
            "email": "dup2@example.com"
        }
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_login_nonexistent_user(db_session):
    """Test login with non-existent username"""
    response = client.post(
        "/users/login",
        json={
            "username": "nonexistent",
            "password": "SomePass123!"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "Invalid" in data["detail"]


def test_register_duplicate_email(db_session):
    """Test that duplicate emails are rejected"""
    # Register first user
    client.post(
        "/users/register",
        json={
            "username": "user1",
            "password": "SecurePass123!",
            "email": "same@example.com"
        }
    )
    
    # Try to register different username with same email
    response = client.post(
        "/users/register",
        json={
            "username": "user2",
            "password": "SecurePass123!",
            "email": "same@example.com"
        }
    )
    
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()