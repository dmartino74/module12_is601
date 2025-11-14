from pydantic import BaseModel, model_validator
from typing import Literal, Optional
from datetime import datetime

# Allow both "Sub" and "Subtract" (tests use both)
OperationType = Literal["Add", "Sub", "Subtract", "Multiply", "Divide"]

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: OperationType

    @model_validator(mode="after")
    def validate_inputs(self):
        if self.type == "Divide" and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: OperationType
    result: Optional[float] = None
    created_at: datetime
    updated_at: datetime

