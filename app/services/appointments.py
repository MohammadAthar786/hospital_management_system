from sqlalchemy.orm import Session 
from app.schemas.appointments import AppointmentCreate,AppointmentUpdate,SmartAppointmentRequest
from app.repositories.appointments import AppointmentRepository
from app.repositories.doctors import DoctorRepository
from app.repositories.doctors_leaves import DoctorLeaveRepository
from fastapi import HTTPException
from app.utils.appointment_algorithm import find_available_slot
from uuid import UUID
from datetime import date
class AppointmentService:
    def __init__(self,db:Session):
        self.appointment_repo=AppointmentRepository(db)
        self.doctor_repo=DoctorRepository(db)
        self.doctor_leave_repo=DoctorLeaveRepository(db)
    
    def get_all_appointments(self):
        return self.appointment_repo.all_appointments()
    def get_appointments_by_id(self,appointment_id:UUID):
        appointment= self.appointment_repo.get_appointment_by_id(appointment_id)
        if not appointment:
            raise HTTPException(status_code=404,detail="appointment not found")
        return appointment
    
    def get_appointment_by_patient_id(self,patient_id:UUID):
        appointments= self.appointment_repo.get_appointments_by_patient_id(patient_id)
        if not appointments:
            raise HTTPException(status_code=404,detail="No appointment found for this patient")
        return appointments
    def get_appointments_by_doctor_id(self,doctor_id:UUID):
        appointments=self.appointment_repo.get_appointments_by_doctor_id(doctor_id)
        if not appointments:
            raise HTTPException(status_code=404,detail="No appointment found for this doctor")
        return appointments
    def get_appointments_on_date(self,appointment_date:date):
        appointments=self.appointment_repo.get_appointments_on_date(appointment_date)
        if not appointments:
            raise HTTPException(status_code=404,detail="No appoitment found on this date")
        return appointments
    def get_appointments_by_status(self,status:str):
        appointments=self.appointment_repo.get_appointments_by_status(status)
        if not appointments:
            raise HTTPException(status_code=404,detail="No appointment found with this status")
        return appointments
    # Smart_booking
    def smart_appointment_book(self,data:SmartAppointmentRequest):
        doctors=self.doctor_repo.get_by_specialty(data.specialty)
        if not doctors:
            raise HTTPException(status_code=404,detail="No doctor found for this specialty")
        doctor_ids = [i.id for i in doctors]
        leaves=self.doctor_leave_repo.get_doctor_leaves_by_date(doctor_ids,data.appointment_date)
        leave_doctor_ids={i.doctor_id for i in leaves}
        available_doctors=[i for i in doctors 
                           if i.id not in leave_doctor_ids]
        if not available_doctors:
            raise HTTPException(status_code=404, detail="No doctor available on this date")
        
        doctor_ids=[i.id for i in available_doctors ]
        
        appointments=self.appointment_repo.get_appointments_by_doctors_on_date(doctor_ids,data.appointment_date)
        
        # algorithm call
        result=find_available_slot(doctors=available_doctors,appointments=appointments,preferred_start_time=data.preferred_start_time)
        
        if not result:
            raise HTTPException(status_code=409,detail="No appointment slot available")
        
        appointment_data={
            "patient_id":data.patient_id,
            "doctor_id":result["doctor_id"],
            "appointment_date":data.appointment_date,
            "start_time":result["start_time"],
            "end_time":result["end_time"],
            "status":"scheduled",
            "notes":  data.reason
            
        }
        return self.appointment_repo.create(appointment_data)
    
    # Manual booking
    def create_appointment(self,data:AppointmentCreate):
        return self.appointment_repo.create(data)
    def update_appointment(self,appointment_id:UUID,data:AppointmentUpdate):
        appointment= self.appointment_repo.update(appointment_id,data)
        if not appointment:
            raise HTTPException(status_code=404,detail="Appointment Not found")
        return self.appointment_repo.delete(appointment_id)
   # deleting
    def delete_appointment(self,appointment_id:UUID):
       appointment=self.appointment_repo.get_appointment_by_id(appointment_id)
       if not appointment:
           raise HTTPException(status_code=404,detail="No appointment found")
       self.appointment_repo.delete(appointment_id)