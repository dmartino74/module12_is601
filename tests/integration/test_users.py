import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/register", json={"username": "testuser", "password": "secret123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_user_success():
    client.post("/users/register", json={"username": "loginuser", "password": "mypassword"})
    response = client.post("/users/login", json={"username": "loginuser", "password": "mypassword"})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

def test_login_user_fail():
    response = client.post("/users/login", json={"username": "wronguser", "password": "badpass"})
    assert response.status_code == 401
