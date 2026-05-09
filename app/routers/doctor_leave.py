from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import date

from app.database import get_db
from app.schemas.doctor_leave import (
    DoctorLeaveCreate,
    DoctorLeaveResponse,
    DoctorLeaveUpdate
)
from app.services.doctor_leaves import DoctorLeaveService
from app.auth.roles import (
    ADMIN,
    STAFF,
    RECEPTION,
    MEDICAL
)
from dependencies.auth import get_current_user, require_role

router = APIRouter(
    prefix="/doctor-leaves",
    tags=["Doctor Leaves"],
    dependencies=[Depends(require_role(STAFF))]
)


@router.get("/", response_model=List[DoctorLeaveResponse])
def get_all_leaves(db: Session = Depends(get_db)):
    service = DoctorLeaveService(db)
    return service.get_all_leaves()


@router.get("/{leave_id}", response_model=DoctorLeaveResponse)
def get_leave_by_id(leave_id: int, db: Session = Depends(get_db)):
    service = DoctorLeaveService(db)
    return service.get_leave_by_id(leave_id)




@router.get("/date/{leave_date}", response_model=List[DoctorLeaveResponse])
def get_leaves_on_date(
    leave_date: date,
    db: Session = Depends(get_db)
):
    service = DoctorLeaveService(db)
    return service.get_doctor_leaves_by_date(leave_date)


@router.get("/doctor/{doctor_id}", response_model=List[DoctorLeaveResponse])
def get_leaves_by_doctor_id(
    doctor_id: UUID,
    db: Session = Depends(get_db)
):
    service = DoctorLeaveService(db)
    return service.get_leave_by_doctor_id(doctor_id)

@router.post("/", response_model=DoctorLeaveResponse)
def create_leave(
    data: DoctorLeaveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(ADMIN))
):
    service = DoctorLeaveService(db)
    return service.create_leave(data)


@router.put("/{leave_id}", response_model=DoctorLeaveResponse)
def update_leave(
    leave_id: int,
    data: DoctorLeaveUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(ADMIN))
):
    service = DoctorLeaveService(db)
    return service.update_leave(leave_id, data)


@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(ADMIN))
):
    service = DoctorLeaveService(db)
    return service.delete_leave(leave_id)