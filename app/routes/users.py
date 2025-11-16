from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.db import get_db
from app.models.user import User
from app.operations.schemas.user_schemas import UserCreate, UserLogin, UserRead, LoginResponse, UserResponse

# Create router with prefix
router = APIRouter(prefix="/users", tags=["users"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT
SECRET_KEY = "supersecretkey"  # 🔧 replace with env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with length validation"""
    encoded = password.encode("utf-8")
    if len(encoded) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes)")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash with length validation"""
    encoded = plain_password.encode("utf-8")
    if len(encoded) > 72:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=UserResponse, status_code=200)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with username, email, and password"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password with length check
    hashed_pw = hash_password(user.password)
    
    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=LoginResponse, status_code=200)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login a user with username and password"""
    # Find user by username (not email)
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(data={"sub": db_user.username, "user_id": db_user.id})
    
    return {
        "message": "Login successful",
        "username": db_user.username,
        "user_id": db_user.id
    }


@router.get("/me", response_model=UserRead)
def get_current_user(db: Session = Depends(get_db)):
    """Get current user information (placeholder - would need JWT token validation)"""
    # This is a placeholder - in production you'd validate the JWT token
    raise HTTPException(status_code=501, detail="Not implemented - requires authentication")