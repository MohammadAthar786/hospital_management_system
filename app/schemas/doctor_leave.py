from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime, date


# 🔹 Base Schema
class DoctorLeaveBase(BaseModel):
    doctor_id: UUID
    leave_date: date
    reason: Optional[str] = None


# 🔹 Create Schema
class DoctorLeaveCreate(DoctorLeaveBase):
    pass


# 🔹 Update Schema
class DoctorLeaveUpdate(BaseModel):
    doctor_id: Optional[UUID] = None
    leave_date: Optional[date] = None
    reason: Optional[str] = None


# 🔹 Response Schema
class DoctorLeaveResponse(DoctorLeaveBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True