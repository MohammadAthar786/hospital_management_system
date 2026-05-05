from sqlalchemy.orm import Session 
from app.schemas.doctor_leave import DoctorLeaveBase,DoctorLeaveResponse,DoctorLeaveCreate,DoctorLeaveUpdate
from app.repositories.doctors_leaves import DoctorLeaveRepository
from app.schemas.doctor_leave import DoctorLeaveBase,DoctorLeaveCreate,DoctorLeaveUpdate,DoctorLeaveResponse 
from fastapi import HTTPException
from uuid import UUID
from datetime import date
class DoctorLeaveService:
    def __init__(self,db:Session):
        self.doctor_leave_repo=DoctorLeaveRepository(db)
    
    
    # get all doctors on leave
    def get_all_leaves(self):
        return self.doctor_leave_repo.get_all()
    
    # Get leave by id 
    def get_leave_by_id(self,leave_id:int):
        leave=self.doctor_leave_repo.get_by_id(leave_id)
        if not leave:
            raise HTTPException(status_code=404,detail="Doctor available")
        return leave
    
    # Get leave by doctor_id
    def get_leave_by_doctor_id(self,doctor_id:UUID):
        leave=self.doctor_leaves_repo.get_leaves_by_doctor_id(doctor_id)
        if not leave:
            raise HTTPException(status_code=404,detail="leave not found for this doctor")
        return leave
      # get Doctors on leave on a particular date 
      
    def get_doctors_on_leave_on_date(self,leave_date:date):
        leaves=self.doctor_leave_repo.get_doctor_leaves_by_date(leave_date)
        if not leaves:
            raise HTTPException(status_code=404,detail="No doctor on leave on this date")
        return leaves
    
    
    # Create Leave 
    
    def create_leave(self,data:DoctorLeaveCreate):
        return self.doctor_leave_repo.create(data)
    
    # Update Leave 
    def update_leave(self,leave_id:int,data:DoctorLeaveUpdate):
        leave=self.doctor_leave_repo.get_by_id(leave_id)
        if not leave:
            raise HTTPException(status_code=404,detail="doctor leave not found")
        update_data=data.model_dump(exclude_unset=True)
        return self.doctor_leave_repo.update(leave_id,update_data)
    
    # Delete Leave 
    def delete_leave(self,leave_id:int):
        leave = self.doctor_leave_repo.get_by_id(leave_id)

        if not leave:
            raise HTTPException(
                status_code=404,
                detail="Doctor leave not found"
            )
        return self.doctor_leave_repo.delete(leave_id)
    