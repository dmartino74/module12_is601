import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ✅ Load DATABASE_URL from environment, fallback to localhost for host-based pytest
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/fastapi_db"
)

# Debug print (optional, remove later)
print("Using DATABASE_URL:", DATABASE_URL)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# ✅ Dependency for FastAPI routes
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
