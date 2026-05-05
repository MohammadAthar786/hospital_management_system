from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.doctor_leave import DoctorLeave
from typing import List
from app.models.doctor import Doctor
from uuid import UUID
from datetime import date
class DoctorLeaveRepository(BaseRepository[DoctorLeave]):
    def __init__(self,db:Session):
        super().__init__(DoctorLeave,db)
    

    # get leaves of doctors by date 
    def get_doctor_leaves_by_date(self, doctor_ids: List[UUID], leave_date: date):
        return (
        self.db.query(DoctorLeave)
        .filter(
            DoctorLeave.doctor_id.in_(doctor_ids),
            DoctorLeave.leave_date == leave_date
        )
        .all()
    )
  
    def get_leaves_by_doctor_id(self,doctor_id:UUID):
        return (self.db.query(DoctorLeave).filter(DoctorLeave.doctor_id==doctor_id).all())
    