from pydantic import BaseModel, EmailStr ##(Special Datatype for  email validation 
# invalid email will not be accepted only valid email will be accepted )
from uuid import UUID
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "patient"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str