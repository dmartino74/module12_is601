from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr   # ✅ include email since your register route expects it
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr   # ✅ include email so response_model matches register route

    class Config:
        from_attributes = True  # ✅ Pydantic v2 replacement for orm_mode
