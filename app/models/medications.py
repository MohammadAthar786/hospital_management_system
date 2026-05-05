from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class Medication(Base):
    __tablename__ = "medications"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id    = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    prescribed_by = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=True)
    drug_name     = Column(String(100), nullable=False)
    dosage        = Column(String(50), nullable=False)
    frequency     = Column(String(50))
    start_date    = Column(Date, nullable=False)
    end_date      = Column(Date, nullable=True)

    patient = relationship("Patient", back_populates="medications")
    doctor  = relationship("Doctor",  back_populates="medications")