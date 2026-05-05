from sqlalchemy import Column, String, Date, Text, ForeignKey, TIMESTAMP,Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id       = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    doctor_id        = Column(UUID(as_uuid=True), ForeignKey("doctors.id"),  nullable=False)
    appointment_date = Column(Date, nullable=False)
    ## Added after 
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status           = Column(String(20), default="scheduled")
    notes            = Column(Text)
    created_at       = Column(TIMESTAMP, server_default=func.now())

    patient          = relationship("Patient", back_populates="appointments")
    doctor           = relationship("Doctor",  back_populates="appointments")
    lab_results      = relationship("LabResult", back_populates="appointment")