from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.appointments import SmartAppointmentRequest,AppointmentUpdate, AppointmentResponse,AppointmentCreate
from app.services.appointments import AppointmentService
from typing import List
from uuid import UUID
from datetime import date
from app.auth.roles import (
    ADMIN,
    STAFF,
    RECEPTION,
    MEDICAL
)
from dependencies.auth import get_current_user, require_role
router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
    dependencies=[Depends(require_role(STAFF))]
)

## smart-booking main feature
@router.post("/smart-book", response_model=AppointmentResponse)
def smart_book_appointment(
    data: SmartAppointmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RECEPTION))
):
    service = AppointmentService(db)
    return service.smart_appointment_book(data)
# Manual appointment create
@router.post("/",response_model=AppointmentResponse)
def create_appointment(data:AppointmentCreate,
                       db:Session=Depends(get_db),
                       current_user=Depends(require_role(RECEPTION))):
    service=AppointmentService(db)
    return service.create_appointment(data)


## Get 
# Get all Appointments 
@router.get("/",response_model=List[AppointmentResponse])
def get_all_appointments(db:Session=Depends(get_db)):
    service=AppointmentService(db)
    return service.get_all_appointments()

# Get appointment by id
@router.get("/appointment/{appointment_id}",response_model=List[AppointmentResponse])
def get_appointments_by_id(appointment_id:UUID,db:Session=Depends(get_db)):
    service=AppointmentService(db)
    return service.get_appointments_by_id(appointment_id)
# get appointment by patient_id
@router.get("/patient/{patient_id}",response_model=List[AppointmentResponse])
def get_appointment_by_patient_id(patient_id:UUID,db:Session=Depends(get_db)):
    service=AppointmentService(db)
    return service.get_appointment_by_patient_id(patient_id)

# Get Appointment by doctor_id
@router.get("/doctor/{doctor_id}",response_model=List[AppointmentResponse])
def get_appointments_by_doctor_id(doctor_id:UUID,db:Session=Depends(get_db)):
    service=AppointmentService(db)
    return service.get_appointments_by_doctor_id(doctor_id)

# Get Appointment by date
@router.get("/date/{appointment_date}",response_model=List[AppointmentResponse])
def get_appointment_by_date(appointment_date:date,db:Session=Depends(get_db)):
    service=AppointmentService(db)
    return service.get_appointments_on_date(appointment_date)

# Get Appointment by status
@router.get("/status/{status}",response_model=List[AppointmentResponse])
def get_appointment_by_status(status:str,db:Session=Depends(get_db)):
    service=AppointmentService(db)
    return service.get_appointments_by_status(status)

# Update Appointments
@router.put("/{appointment_id}",response_model=AppointmentResponse)
def update_appointment(appointment_id:UUID,
                       data:AppointmentUpdate,
                       db:Session=Depends(get_db),
                       current_user=Depends(require_role(RECEPTION))):
    service=AppointmentService(db)
    return service.update(appointment_id,data)

# Delete Appointments
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id:UUID,
                       db:Session=Depends(get_db),
                       current_user=Depends(require_role(ADMIN))):
    service=AppointmentService(db)
    return service.delete_appointment(appointment_id)