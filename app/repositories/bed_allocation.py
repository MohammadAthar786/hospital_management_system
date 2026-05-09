from sqlalchemy.orm import Session
from app.models.bed_allocation import BedAllocation
from app.repositories.base import BaseRepository
from typing import List
from uuid import UUID
from datetime import date,datetime

class BedAllocationRepository(BaseRepository[BedAllocation]):
    def __init__(self,db:Session):
        super().__init__(BedAllocation,db)
        
        
    def get_allocation_by_id(self,allocation_id:int):
        return self.db.query(BedAllocation).filter(BedAllocation.id==allocation_id).first()
    
    def get_allocation_by_patient_id(self,patient_id:UUID):
        return self.db.query(BedAllocation).filter(BedAllocation.patient_id==patient_id).all()
    
    def get_allocation_by_bed_id(self,bed_id:int):
        return self.db.query(BedAllocation).filter(BedAllocation.bed_id==bed_id).all()
    
    def get_allocation_by_allocated_date(self,allocated_date:datetime):
        return self.db.query(BedAllocation).filter(BedAllocation.allocated_at==allocated_date).all()
    
    def get_allocations_by_released_date(self,released_date:datetime):
        return self.db.query(BedAllocation).filter(BedAllocation.released_at==released_date).all()