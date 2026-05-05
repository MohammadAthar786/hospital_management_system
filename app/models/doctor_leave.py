from sqlalchemy import Column, String, Integer, TIMESTAMP, BOOLEAN, ForeignKey, DateTime,Date
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class DoctorLeave(Base):
    __tablename__ = "doctor_leaves"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)

    leave_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)