from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.bed_allocation import BedAllocationService
from app.schemas.bed_allocation import BedAllocationCreate, BedAllocationResponse
from uuid import UUID
from datetime import datetime
from typing import List
from app.auth.roles import (
    ADMIN,
    STAFF,
    RECEPTION,
    MEDICAL
)
from dependencies.auth import get_current_user, require_role
router = APIRouter(
    prefix="/bed-allocations",
    tags=["Bed Allocations"],
    dependencies=[Depends(require_role(RECEPTION))]
)



def get_service(db: Session = Depends(get_db)) -> BedAllocationService:
    return BedAllocationService(db)


# GET /bed-allocations/{allocation_id}
@router.get("/{allocation_id}", response_model=BedAllocationResponse)
def get_allocation_by_id(
    allocation_id: int,
    service: BedAllocationService = Depends(get_service)
):
    return service.get_allocation_by_id(allocation_id)


# GET /bed-allocations/bed/{bed_id}
@router.get("/bed/{bed_id}", response_model=List[BedAllocationResponse])
def get_allocations_by_bed_id(
    bed_id: int,
    service: BedAllocationService = Depends(get_service)
):
    return service.get_allocations_by_bed_id(bed_id)


# GET /bed-allocations/patient/{patient_id}
@router.get("/patient/{patient_id}", response_model=List[BedAllocationResponse])
def get_allocations_by_patient_id(
    patient_id: UUID,
    service: BedAllocationService = Depends(get_service)
):
    return service.get_allocations_by_patient_id(patient_id)


# GET /bed-allocations/by-date/allocated?allocated_date=2024-01-01T00:00:00
@router.get("/by-date/allocated", response_model=List[BedAllocationResponse])
def get_allocations_by_allocation_date(
    allocated_date: datetime,
    service: BedAllocationService = Depends(get_service)
):
    return service.get_allocations_by_allocation_date(allocated_date)


# GET /bed-allocations/by-date/released?released_date=2024-01-01T00:00:00
@router.get("/by-date/released", response_model=List[BedAllocationResponse])
def get_allocations_by_released_date(
    released_date: datetime,
    service: BedAllocationService = Depends(get_service)
):
    return service.get_allocations_by_released_date(released_date)


# POST /bed-allocations/allocate
@router.post("/allocate", response_model=BedAllocationResponse, status_code=201)
def allocate_bed(
    data: BedAllocationCreate,
    service: BedAllocationService = Depends(get_service)
):
    return service.allocate_bed(data)


# PATCH /bed-allocations/{allocation_id}/release
@router.patch("/{allocation_id}/release", response_model=BedAllocationResponse)
def release_bed(
    allocation_id: int,
    service: BedAllocationService = Depends(get_service)
):
    return service.release_bed(allocation_id)