from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db import engine
from app.models.base import Base
from app.routes import calculations, users  # Import both routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Clean up resources if needed
    pass


# Create FastAPI app with lifespan
app = FastAPI(
    title="Calculator API",
    description="A simple calculator API with user authentication and calculation history",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)  # This adds /users/register and /users/login
app.include_router(calculations.router)  # This adds /calculations endpoints


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Calculator API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}