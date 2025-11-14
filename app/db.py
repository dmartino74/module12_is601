import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Use environment variable if set, otherwise default to local Postgres
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

# ✅ Create engine
# echo=True → logs SQL statements (helpful for debugging)
# future=True → enables SQLAlchemy 2.0 style usage
engine = create_engine(DATABASE_URL, echo=True, future=True)

# ✅ Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Shared Base class for all models
Base = declarative_base()

# ✅ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Initialize tables (useful for dev/tests)
def init_db():
    # Import models so they are registered with Base
    from app.models import calculation, user
    Base.metadata.create_all(bind=engine)
