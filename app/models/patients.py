from sqlalchemy import Column, String, Integer, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(String(100), nullable=False)
    age           = Column(Integer, nullable=False)
    gender        = Column(String(10))
    blood_pressure = Column(Numeric(5, 2))
    cholesterol   = Column(Numeric(6, 2))
    blood_sugar   = Column(Numeric(6, 2))
    email         = Column(String(150), unique=True)
    phone         = Column(String(15))
    created_at    = Column(TIMESTAMP, server_default=func.now())

    # Relationships — lets you do patient.appointments in Python
    appointments  = relationship("Appointment", back_populates="patient")
    lab_results   = relationship("LabResult",   back_populates="patient")
    medications   = relationship("Medication",  back_populates="patient")
    bed_allocations = relationship("BedAllocation",back_populates="patient")