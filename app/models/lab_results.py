from sqlalchemy import Column, String, Date, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class LabResult(Base):
    __tablename__ = "lab_results"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id     = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=True)
    test_name      = Column(String(100), nullable=False)
    result_value   = Column(Numeric(8, 2), nullable=False)
    unit           = Column(String(30))
    normal_min     = Column(Numeric(8, 2))
    normal_max     = Column(Numeric(8, 2))
    tested_at      = Column(Date, nullable=False, server_default=func.now())

    patient     = relationship("Patient",     back_populates="lab_results")
    appointment = relationship("Appointment", back_populates="lab_results")