from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.calculation import Calculation

router = APIRouter()

@router.post("/calculate")
def calculate(a: float, b: float, type: str, db: Session = Depends(get_db)):
    # Normalize input
    operation = type.lower()

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = a / b
    else:
        raise HTTPException(status_code=400, detail="Unsupported operation type")

    # Save to DB
    calc = Calculation(a=a, b=b, type=operation, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)

    return {
        "id": calc.id,
        "a": calc.a,
        "b": calc.b,
        "type": calc.type,
        "result": calc.result,
        "created_at": calc.created_at
    }
