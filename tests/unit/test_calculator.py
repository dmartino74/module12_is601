import pytest
from fastapi import HTTPException
from app.operations import perform_operation, get_operation

@pytest.mark.parametrize("a, b, op_type, expected", [
    (10, 5, "Add", 15),
    (-10, -5, "Add", -15),
    (5.5, 2.5, "Add", 8.0),
    (10, 5, "Sub", 5),
    (-10, -5, "Sub", -5),
    (5.5, 2.2, "Sub", 3.3),
    (10, 5, "Multiply", 50),
    (-10, -5, "Multiply", 50),
    (2.5, 4.0, "Multiply", 10.0),
    (10, 2, "Divide", 5.0),
    (5.5, 2.2, "Divide", 2.5),
])
def test_operations(a, b, op_type, expected):
    result = perform_operation(a, b, op_type)
    assert result == pytest.approx(expected)

def test_divide_by_zero():
    with pytest.raises(HTTPException) as exc_info:
        perform_operation(10, 0, "Divide")
    assert exc_info.value.status_code == 400
    assert "Cannot divide by zero" in str(exc_info.value.detail)

def test_invalid_operation():
    with pytest.raises(ValueError, match="Invalid operation type"):
        perform_operation(10, 5, "foo")

def test_get_operation_subtract_alias():
    op = get_operation("Subtract")
    result = op.compute(10, 3)
    assert result == 7

