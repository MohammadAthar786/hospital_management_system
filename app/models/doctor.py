from sqlalchemy import Column, String, TIMESTAMP,Integer,Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name         = Column(String(100), nullable=False)
    specialty    = Column(String(100), nullable=False)
    email        = Column(String(150), unique=True, nullable=False)
    phone        = Column(String(15))
    created_at   = Column(TIMESTAMP, server_default=func.now())
    experience   = Column(Integer,nullable=False,default=0)
    appointments = relationship("Appointment", back_populates="doctor")
    medications  = relationship("Medication",  back_populates="doctor")
    ## Added after 
    available_from = Column(Time, nullable=True)
    available_to   = Column(Time, nullable=True)
    slot_duration  = Column(Integer, default=30)  # minutes