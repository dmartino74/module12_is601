from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_calculate_add(db_session):
    """Test addition calculation"""
    response = client.post(
        "/calculations",
        json={"a": 5, "b": 3, "type": "add"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 8
    assert data["type"] == "add"


def test_calculate_subtract(db_session):
    """Test subtraction calculation"""
    response = client.post(
        "/calculations",
        json={"a": 10, "b": 4, "type": "subtract"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 6


def test_calculate_multiply(db_session):
    """Test multiplication calculation"""
    response = client.post(
        "/calculations",
        json={"a": 7, "b": 6, "type": "multiply"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 42


def test_calculate_divide(db_session):
    """Test division calculation"""
    response = client.post(
        "/calculations",
        json={"a": 20, "b": 5, "type": "divide"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 4.0


def test_calculate_divide_by_zero(db_session):
    """Test division by zero returns error"""
    response = client.post(
        "/calculations",
        json={"a": 10, "b": 0, "type": "divide"}
    )
    
    # Should return 400 or 422 error
    assert response.status_code in [400, 422]
    data = response.json()
    
    # Check for error in detail
    assert "detail" in data
    detail = str(data["detail"]).lower()
    assert "divide" in detail or "division" in detail or "zero" in detail


def test_calculate_invalid_type(db_session):
    """Test invalid calculation type returns error"""
    response = client.post(
        "/calculations",
        json={"a": 10, "b": 5, "type": "invalid"}
    )
    
    # Should return 422 validation error
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_calculations(db_session):
    """Test getting all calculations"""
    # First create a calculation
    client.post(
        "/calculations",
        json={"a": 5, "b": 3, "type": "add"}
    )
    
    # Then get all calculations
    response = client.get("/calculations")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_calculation_by_id(db_session):
    """Test getting a specific calculation by ID"""
    # Create a calculation
    create_response = client.post(
        "/calculations",
        json={"a": 5, "b": 3, "type": "add"}
    )
    calc_id = create_response.json()["id"]
    
    # Get it by ID
    response = client.get(f"/calculations/{calc_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["result"] == 8


def test_update_calculation(db_session):
    """Test updating a calculation"""
    # Create a calculation
    create_response = client.post(
        "/calculations",
        json={"a": 5, "b": 3, "type": "add"}
    )
    calc_id = create_response.json()["id"]
    
    # Update it
    response = client.put(
        f"/calculations/{calc_id}",
        json={"a": 10, "b": 5, "type": "multiply"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 50


def test_delete_calculation(db_session):
    """Test deleting a calculation"""
    # Create a calculation
    create_response = client.post(
        "/calculations",
        json={"a": 5, "b": 3, "type": "add"}
    )
    calc_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/calculations/{calc_id}")
    
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/calculations/{calc_id}")
    assert get_response.status_code == 404