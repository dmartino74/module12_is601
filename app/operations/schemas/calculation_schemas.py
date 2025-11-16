from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CalculationCreate(BaseModel):
    """Schema for creating a new calculation"""
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")
    type: str = Field(..., description="Operation type: add, subtract, multiply, divide")
    
    class Config:
        json_schema_extra = {
            "example": {
                "a": 10.0,
                "b": 5.0,
                "type": "add"
            }
        }


class CalculationRead(BaseModel):
    """Schema for reading a calculation from database"""
    id: int
    a: float
    b: float
    type: str
    result: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Backwards compatibility aliases
CalculationRequest = CalculationCreate
CalculationResponse = CalculationRead