from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.calculation import Calculation
from app.operations.schemas.calculation_schemas import CalculationCreate, CalculationRead

# IMPORTANT: Use /calculations (plural) not /calculate
router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("", response_model=List[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    """
    BROWSE: Get all calculations (GET /calculations)
    """
    calculations = db.query(Calculation).all()
    return calculations


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(calculation_id: int, db: Session = Depends(get_db)):
    """
    READ: Get a single calculation by ID (GET /calculations/{id})
    """
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation


@router.post("", response_model=CalculationRead, status_code=200)
def add_calculation(calc: CalculationCreate, db: Session = Depends(get_db)):
    """
    ADD: Create a new calculation (POST /calculations)
    """
    # Validate operation type
    valid_types = ["add", "subtract", "multiply", "divide"]
    if calc.type.lower() not in valid_types:
        raise HTTPException(
            status_code=422, 
            detail=f"Invalid operation type '{calc.type}'. Must be one of: {valid_types}"
        )
    
    # Perform calculation
    op_type = calc.type.lower()
    
    try:
        if op_type == "add":
            result = calc.a + calc.b
        elif op_type == "subtract":
            result = calc.a - calc.b
        elif op_type == "multiply":
            result = calc.a * calc.b
        elif op_type == "divide":
            if calc.b == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = calc.a / calc.b
        else:
            raise HTTPException(status_code=422, detail="Invalid operation type")
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    
    # Save to database
    new_calc = Calculation(
        a=calc.a,
        b=calc.b,
        type=op_type,
        result=result
    )
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    
    return new_calc


@router.put("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(calculation_id: int, calc: CalculationCreate, db: Session = Depends(get_db)):
    """
    EDIT: Update an existing calculation (PUT /calculations/{id})
    """
    # Find existing calculation
    db_calc = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    # Validate operation type
    valid_types = ["add", "subtract", "multiply", "divide"]
    op_type = calc.type.lower()
    
    if op_type not in valid_types:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid operation type '{calc.type}'. Must be one of: {valid_types}"
        )
    
    # Recalculate
    try:
        if op_type == "add":
            result = calc.a + calc.b
        elif op_type == "subtract":
            result = calc.a - calc.b
        elif op_type == "multiply":
            result = calc.a * calc.b
        elif op_type == "divide":
            if calc.b == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = calc.a / calc.b
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    
    # Update fields
    db_calc.a = calc.a
    db_calc.b = calc.b
    db_calc.type = op_type
    db_calc.result = result
    
    db.commit()
    db.refresh(db_calc)
    
    return db_calc


@router.delete("/{calculation_id}")
def delete_calculation(calculation_id: int, db: Session = Depends(get_db)):
    """
    DELETE: Remove a calculation (DELETE /calculations/{id})
    """
    db_calc = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    db.delete(db_calc)
    db.commit()
    
    return {"message": "Calculation deleted successfully", "id": calculation_id}