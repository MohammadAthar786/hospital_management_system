from sqlalchemy.orm import Session 
from fastapi import APIRouter,Depends
from app.database import get_db
from app.models.bed import Bed
from app.schemas.bed import BedBase,BedCreate,BedResponse,BedUpdate
from app.services.bed import BedService
from uuid import UUID
from datetime import date
from typing import List
from app.auth.roles import (
    ADMIN,
    STAFF,
    RECEPTION,
    MEDICAL
)
from dependencies.auth import get_current_user, require_role


router = APIRouter(
    prefix="/bed",
    tags=["Bed information"],
    dependencies=[Depends(require_role(RECEPTION))]
)

## Get Method

@router.get("/",response_model=List[BedResponse])
def all_beds(db:Session=Depends(get_db)):
    service=BedService(db)
    return service.get_all_bed()

@router.get("/ward/{ward}",response_model=List[BedResponse])
def get_all_beds_by_ward(ward:str,db:Session=Depends(get_db)):
    service=BedService(db)
    return service.get_bed_by_ward(ward)
@router.get("/bed_type/{bed_type}",response_model=List[BedResponse])
def get_bed_by_bed_type(bed_type:str,db:Session=Depends(get_db)):
    service=BedService(db)
    return service.get_bed_by_bed_type(bed_type)

@router.get("/bed_id{bed_id}",response_model=BedResponse)
def get_bed_by_bed_id(bed_id:int,db:Session=Depends(get_db)):
    service=BedService(db)
    return service.get_by_bed_id(bed_id)
@router.get("/available_bed",response_model=List[BedResponse])
def all_available_bed(db:Session=Depends(get_db)):
    service=BedService(db)
    return service.check_available_bed()
## Post
@router.post("/")
def create_bed(data:BedCreate,
               db:Session=Depends(get_db),
               current_user=Depends(require_role(ADMIN))):
    service=BedService(db)
    return service.create_bed(data)

## Put
@router.put("/")
def update_bed(data:BedUpdate,
               db:Session=Depends(get_db),
               current_user=Depends(require_role(ADMIN))):
    service=BedService(db)
    return service.update_bed(data)