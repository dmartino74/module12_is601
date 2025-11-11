from pydantic import BaseModel, model_validator
from typing import Literal, Optional
from datetime import datetime

# Define allowed operation types
OperationType = Literal["Add", "Sub", "Multiply", "Divide"]

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: OperationType

    @model_validator(mode="after")
    def validate_inputs(cls, values):
        if values.type == "Divide" and values.b == 0:
            raise ValueError("Cannot divide by zero")
        return values

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: OperationType
    result: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
