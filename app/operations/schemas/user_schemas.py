from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=72)  # bcrypt limit is 72 bytes
    email: EmailStr
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        """Ensure password doesn't exceed bcrypt's 72-byte limit"""
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v


class UserLogin(BaseModel):
    """Schema for user login - only requires username and password"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=72)
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        """Ensure password doesn't exceed bcrypt's 72-byte limit"""
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v


class UserRead(BaseModel):
    """Schema for returning complete user data (without password)"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response after registration (simplified)"""
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Schema for login response"""
    message: str
    username: str
    user_id: Optional[int] = None