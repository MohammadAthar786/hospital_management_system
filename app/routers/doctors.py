from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.services.doctors import DoctorService
from app.schemas.doctors import DoctorCreate, DoctorResponse, DoctorUpdate
from app.auth.roles import (
    ADMIN,
    STAFF,
    RECEPTION,
    MEDICAL
)
from dependencies.auth import get_current_user, require_role

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
    dependencies=[Depends(require_role(STAFF))]
)



@router.get("/", response_model=List[DoctorResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    service = DoctorService(db)
    return service.get_all_doctors()


@router.get("/specialty/{specialty}", response_model=List[DoctorResponse])
def get_by_specialty(specialty: str, db: Session = Depends(get_db)):
    service = DoctorService(db)
    return service.get_doctor_by_specialty(specialty)


@router.get("/specialty/{specialty}/count")
def count_doctors_by_specialty(specialty: str, db: Session = Depends(get_db)):
    service = DoctorService(db)
    return service.specialty_count(specialty)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor_by_id(doctor_id: UUID, db: Session = Depends(get_db)):
    service = DoctorService(db)
    return service.get_doctor_by_id(doctor_id)


@router.post("/", response_model=DoctorResponse)
def create_doctor(data: DoctorCreate, 
                  db: Session = Depends(get_db),
                  current_user=Depends(require_role(ADMIN))):
    service = DoctorService(db)
    return service.create_doctor(data)


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: UUID, 
                  data: DoctorUpdate, 
                  db: Session = Depends(get_db),
                  current_user=Depends(require_role(ADMIN))):
    service = DoctorService(db)
    return service.update_doctor(doctor_id, data)


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: UUID, 
                  db: Session = Depends(get_db),
                  current_user=Depends(require_role(ADMIN))
                  ):
    service = DoctorService(db)
    service.delete_doctor(doctor_id)
    return {"message": "Doctor deleted successfully"}