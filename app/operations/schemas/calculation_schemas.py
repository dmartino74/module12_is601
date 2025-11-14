from pydantic import BaseModel

class CalculationRequest(BaseModel):
    a: float
    b: float
    type: str   # plain string, route handles validation

class CalculationResponse(BaseModel):
    result: float
