from sqlalchemy import create_engine
from app.models.base import Base   # ✅ shared Base from app/models/__init__.py
from app.db import engine     # ✅ use your existing engine setup

# Create all tables defined in models
def create_all_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all_tables()
    print("✅ Tables created successfully.")
