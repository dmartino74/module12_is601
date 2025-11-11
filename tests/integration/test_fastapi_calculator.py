import pytest
from fastapi.testclient import TestClient
from app.main import app  # ✅ Fixed import path

client = TestClient(app)

@pytest.mark.parametrize("a,b,type,result", [
    (10, 5, "Add", 15),
    (10, 5, "Sub", 5),
    (10, 5, "Subtract", 5),
    (10, 5, "Multiply", 50),
    (10, 5, "Divide", 2),
])
def test_calculate_success(a, b, type, result):
    response = client.post("/calculate", json={"a": a, "b": b, "type": type})
    assert response.status_code == 200
    assert response.json()["result"] == result

def test_calculate_invalid_type():
    response = client.post("/calculate", json={"a": 10, "b": 5, "type": "foo"})
    assert response.status_code == 400
    assert "Unsupported operation type" in response.json()["error"]

def test_calculate_divide_by_zero():
    response = client.post("/calculate", json={"a": 10, "b": 0, "type": "Divide"})
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["error"]
