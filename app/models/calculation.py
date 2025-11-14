from sqlalchemy import Column, Integer, Float, String, DateTime, func
from app.db import Base  # ✅ shared Base

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String(50), nullable=False)   # ✅ operation type (add, subtract, etc.)
    result = Column(Float, nullable=False)      # ✅ calculation result
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)



