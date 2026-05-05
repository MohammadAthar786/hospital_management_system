from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime,date,time
class AppointmentBase(BaseModel):
    patient_id: UUID
    doctor_id: UUID
    appointment_date: date
    start_time: time
    end_time: time
    status: Optional[str] = None 
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass
class AppointmentUpdate(BaseModel):
    doctor_id: Optional[UUID] = None
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class SmartAppointmentRequest(BaseModel):
        patient_id: UUID
        specialty: str
        appointment_date: date
        preferred_start_time: Optional[time] = None
        reason: Optional[str] = None
        
class AppointmentResponse(AppointmentBase):
    id: UUID
    created_at: datetime

    class Config:
      from_attributes=True