from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.appointments import Appointment
from typing import List
from uuid import UUID
from datetime import date
from sqlalchemy import func
class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self,db:Session):
        super().__init__(Appointment,db)
    
    def all_appointments(self)->List[Appointment]:
        return self.db.query(Appointment).all()
        
    # Required for smart_appointment algorithm 
    def get_appointments_by_doctors_on_date(self,doctor_ids:List[UUID],appointment_date:date)->List[Appointment]:
         return (
        self.db.query(Appointment)
        .filter(
            Appointment.doctor_id.in_(doctor_ids),
            Appointment.appointment_date == appointment_date
        )
        .all()   # ⚠️ YE MOST IMPORTANT HAI
    )
    def get_appointments_by_patient_id(self,patient_id:UUID)->List[Appointment]:
        return  self.db.query(Appointment).filter(Appointment.patient_id==patient_id).all()
      
    def get_appointments_by_doctor_id(self,doctor_id:UUID)->List[Appointment]:
        return self.db.query(Appointment).filer(Appointment.doctor_id==doctor_id).all()
        
    def get_appointments_on_date(self,appointment_date:date)->List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.appointment_date==appointment_date).all()
       
    def get_appointments_by_status(self,status:str)->List[Appointment]:
        return self.db.query(Appointment).filter(func.lower(Appointment.status)==status.lower()).all()
        
    def get_appointment_by_id(self,appointment_id:UUID):
        return self.db.query(Appointment).filter(Appointment.id==appointment_id)
    