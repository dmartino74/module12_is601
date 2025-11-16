import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.base import Base  # ✅ Import Base instead of creating it

# Load DATABASE_URL from environment, fallback to localhost
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/fastapi_db"
)

# Debug print (optional, can remove later)
print("Using DATABASE_URL:", DATABASE_URL)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db():
    """
    Dependency that provides a database session to FastAPI routes.
    Automatically closes the session after the request is complete.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()