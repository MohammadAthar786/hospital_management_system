from sqlalchemy import Column, String, Integer, TIMESTAMP, BOOLEAN, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class BedAllocation(Base):
    __tablename__ = "bed_allocation"
    
    id           = Column(Integer, primary_key=True, index=True)
    patient_id   = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    bed_id       = Column(Integer, ForeignKey("bed.id"), nullable=False)
    allocated_at = Column(DateTime, default=datetime.utcnow,nullable=False)
    released_at  = Column(DateTime, nullable=True)  #  default=True bhi galat tha

    #  Class name - capital letter
    patient = relationship("Patient",back_populates="bed_allocations")
    bed     = relationship("Bed",back_populates="bed_allocations")