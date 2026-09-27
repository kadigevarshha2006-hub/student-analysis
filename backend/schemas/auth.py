from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120, example="Jane Doe")
    email: EmailStr = Field(..., example="jane.doe@example.com")
    password: str = Field(..., min_length=6, max_length=100, example="StrongPassword123!")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="jane.doe@example.com")
    password: str = Field(..., example="StrongPassword123!")

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
