from typing import Union
from fastapi import HTTPException  # ✅ Added for proper error handling

Number = Union[int, float]

class Operation:
    def compute(self, a: Number, b: Number) -> Number:
        raise NotImplementedError("Subclasses must implement compute method.")

class AddOperation(Operation):
    def compute(self, a: Number, b: Number) -> Number:
        return a + b

class SubOperation(Operation):
    def compute(self, a: Number, b: Number) -> Number:
        return a - b

class MultiplyOperation(Operation):
    def compute(self, a: Number, b: Number) -> Number:
        return a * b

class DivideOperation(Operation):
    def compute(self, a: Number, b: Number) -> float:
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero!")  # ✅ Fixed message
        return a / b

def get_operation(op_type: str) -> Operation:
    operations = {
        "Add": AddOperation(),
        "Sub": SubOperation(),
        "Subtract": SubOperation(),  # ✅ Alias added
        "Multiply": MultiplyOperation(),
        "Divide": DivideOperation()
    }
    if op_type not in operations:
        raise ValueError(f"Invalid operation type: {op_type}")
    return operations[op_type]

def perform_operation(a: Number, b: Number, op_type: str) -> Number:
    return get_operation(op_type).compute(a, b)
