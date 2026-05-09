from sqlalchemy.orm import Session 
from  app.repositories.bed import BedRepository
from app.schemas.bed import BedCreate,BedResponse,BedUpdate
from uuid import UUID
from datetime import date,datetime

class BedService:
    def __init__(self,db:Session):
        self.bed_repo=BedRepository(db)
        
    def get_all_bed(self):
        return self.bed_repo.get_all()
    def get_bed_by_ward(self,ward:str):
        return self.bed_repo.get_by_ward(ward)
    def get_bed_by_bed_type(self,bed_type:str):
        return self.bed_repo.get_by_bed_type(bed_type)
    def get_by_bed_id(self,bed_id:int):
        return self.bed_repo.get_by_id(bed_id)
    def check_available_bed(self):
        return self.bed_repo.check_availble_bed()
    
    def create_bed(self,data:BedCreate):
        return self.bed_repo.create(data)
    
    def update_bed(self,data:BedUpdate):
        return self.bed_repo.update(data)
    