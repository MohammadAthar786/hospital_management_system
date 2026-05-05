from sqlalchemy.orm import Session 
from app.schemas.doctors import DoctorCreate,DoctorUpdate
from app.repositories.doctors import DoctorRepository
from fastapi import HTTPException

class DoctorService:
    def __init__(self,db:Session):
        self.repo=DoctorRepository(db)
        
    def get_all_doctors(self):
        return self.repo.get_all()
    def get_doctor_by_id(self,doctor_id):
        doctor=self.repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404,detail="doctor not found")
        return doctor
   
    def create_doctor(self,data:DoctorCreate):
        existing_email=self.repo.get_by_email(data.email)
        if existing_email:
            raise HTTPException(status_code=400,detail="Doctor with this email already exist")
        existing_phone=self.repo.get_by_phone(data.phone)
        if existing_phone:
            raise HTTPException(status_code=400,detail="Doctor with this phone already exist")
        return self.repo.create(data)
    def update_doctor(self,doctor_id,data:DoctorUpdate):
        doctor=self.repo.get_by_id(doctor_id)
        if not doctor :
            raise HTTPException(status_code=404,detail="doctor not found")
        return self.repo.update(doctor_id,data)
    def delete_doctor(self,doctor_id):
        doctor=self.repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404,detail="Doctor not Found")
        return self.repo.delete(doctor_id)
    
    
    def specialty_count(self,specialty):
        count=self.repo.count_by_specialty(specialty)
        return {
            "specialty":specialty,
            "count":count
        }
    def get_doctor_by_specialty(self,specialty):
        doctors=self.repo.get_by_specialty(specialty)
        if not doctors:
            raise HTTPException(status_code=404,detail="No doctor found for this specialty")
        return doctors