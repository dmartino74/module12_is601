from typing import Union
from fastapi import HTTPException

Number = Union[int, float]


class Operation:
    def compute(self, a: Number, b: Number) -> Number:
        raise NotImplementedError("Subclasses must implement compute()")


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
            # ✅ Match test expectation exactly
            raise HTTPException(status_code=400, detail="Error: Cannot divide by zero!")
        return a / b


# Factory function to get the right operation class
def get_operation(op_type: str) -> Operation:
    op_type = op_type.lower()
    if op_type in ("add",):
        return AddOperation()
    elif op_type in ("sub", "subtract"):
        return SubOperation()
    elif op_type in ("multiply",):
        return MultiplyOperation()
    elif op_type in ("divide",):
        return DivideOperation()
    else:
        raise ValueError("Invalid operation type")


# Convenience function to perform an operation directly
def perform_operation(a: Number, b: Number, op_type: str) -> Number:
    operation = get_operation(op_type)
    return operation.compute(a, b)
