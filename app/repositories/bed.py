from app.models.bed import Bed
from app.repositories.base import BaseRepository
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date,datetime

class BedRepository(BaseRepository[Bed]):
    def __init__(self,db:Session):
        super().__init__(Bed,db)
    
    def get_by_ward(self,ward:str):
        return self.db.query(Bed).filter(Bed.ward==ward).all()
    def get_by_bed_type(self,bed_type:str):
        return self.db.query(Bed).filter(Bed.bed_type==bed_type).all()
    
    def check_available_bed_id(self,bed_id:int):
         return self.db.query(Bed).filter(
            Bed.id == bed_id,
            Bed.is_available == True
        ).first()
        
    def check_availble_bed(self):
        return self.db.query(Bed).filter(Bed.is_available==True).all()
    