from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

# Base — shared fields
class PatientBase(BaseModel):
    name:           str
    age:            int
    gender:         Optional[str] = None
    blood_pressure: Optional[float] = None
    cholesterol:    Optional[float] = None
    blood_sugar:    Optional[float] = None
    email:          Optional[EmailStr] = None
    phone:          Optional[str] = None

# Create — what the API accepts when creating a patient
class PatientCreate(PatientBase):
    pass

# Update — all fields optional for partial updates
class PatientUpdate(BaseModel):
    name:           Optional[str] = None
    age:            Optional[int] = None
    blood_pressure: Optional[float] = None
    cholesterol:    Optional[float] = None
    blood_sugar:    Optional[float] = None

# Response — what the API sends back (includes id + created_at)
class PatientResponse(PatientBase):
    id:         UUID
    created_at: datetime

    class Config:
        from_attributes = True  # Lets Pydantic read SQLAlchemy objects