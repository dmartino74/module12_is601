from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Calculation
from app.operations.schemas.calculation_schemas import CalculationRequest, CalculationResponse

router = APIRouter(prefix="/calculate", tags=["calculations"])

@router.post("", response_model=CalculationResponse)
def calculate(request: CalculationRequest, db: Session = Depends(get_db)):
    a, b, op_type = request.a, request.b, request.type.lower()

    # Supported operations
    valid_ops = ["add", "subtract", "sub", "multiply", "divide"]
    if op_type not in valid_ops:
        raise HTTPException(status_code=400, detail="Unsupported operation type")

    # Divide by zero check
    if op_type == "divide" and b == 0:
        raise HTTPException(status_code=400, detail="Error: Cannot divide by zero!")

    # Perform calculation
    if op_type == "add":
        result = a + b
    elif op_type in ["sub", "subtract"]:
        result = a - b
    elif op_type == "multiply":
        result = a * b
    elif op_type == "divide":
        result = a / b

    # Save to DB
    calc = Calculation(a=a, b=b, type=op_type, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)

    # Return response model
    return CalculationResponse(
        id=calc.id,
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=calc.result,
        created_at=calc.created_at
    )

