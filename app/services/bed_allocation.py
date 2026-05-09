from sqlalchemy.orm import Session 
from app.models.bed_allocation import BedAllocation
from app.repositories.bed import BedRepository
from app.repositories.bed_allocation import BedAllocationRepository
from fastapi import HTTPException
from app.schemas.bed_allocation  import BedAllocationCreate
from uuid import UUID
from datetime import datetime

class BedAllocationService:
    def __init__(self,db:Session):
        self.bed_allocation_repo=BedAllocationRepository(db)
        self.bed_repo=BedRepository(db)
        
    def get_allocation_by_id(self,allocation_id:int ):
        allocation = self.bed_allocation_repo.get_allocation_by_id(allocation_id)
        if not allocation:
            raise HTTPException(status_code=404, detail="Bed allocation not found")

        return allocation
    
    def get_allocations_by_bed_id(self,bed_id:int):
        allocations=self.bed_allocation_repo.get_allocation_by_bed_id(bed_id)
        if not allocations:
            raise HTTPException(status_code=404,detail="Bed allocation not found")
        return allocations
    def get_allocations_by_patient_id(self,patient_id:UUID):
        allocations=self.bed_allocation_repo.get_allocation_by_patient_id(patient_id)
        if not allocations:
            raise HTTPException(status_code=404,detail="No Bed allocated for this patient")
        return allocations
    def get_allocations_by_allocation_date(self,allocated_date:datetime):
        allocations=self.bed_allocation_repo.get_allocation_by_allocated_date(allocated_date)
        if not allocations:
            raise HTTPException(status_code=404,detail="No allocations on this date")
        return allocations
    def get_allocations_by_released_date(self,released_date:datetime):
        allocations=self.bed_allocation_repo.get_allocations_by_released_date(released_date)
        if not allocations:
            raise HTTPException(status_code=404,detail="Not released")
        return allocations
    def allocate_bed(self,data:BedAllocationCreate):
        bed=self.bed_repo.check_available_bed_id(data.bed_id)
        if not bed:
            raise HTTPException(status_code=400,detail="Bed not found or bed not available")
        allocation=self.bed_allocation_repo.create(data)
        bed.is_available=False
        self.bed_allocation_repo.db.commit()
        self.bed_allocation_repo.refresh(bed)
        self.bed_allocation_repo.refresh(allocation)

        return allocation
    def release_bed(self,allocation_id:int):
        allocation = self.get_allocation_by_id(allocation_id)

        if allocation.released_at is not None:
            raise HTTPException(status_code=400, detail="Bed already released")

        allocation.released_at = datetime.utcnow()
        allocation.bed.is_available = True

        self.bed_allocation_repo.db.commit()
        self.bed_allocation_repo.db.refresh(allocation)

        return allocation