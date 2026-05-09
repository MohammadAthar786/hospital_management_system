from sqlalchemy import String,Column,TIMESTAMP,Integer,Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Bed(Base):
    __tablename__="bed"
    id =Column(Integer,primary_key=True,index=True)
    ward=Column(String,nullable=False)
    bed_number=Column(String,unique=True,nullable=False)
    bed_type=Column(String,nullable=False) # ICU ,General,Emergency
    is_available=Column(Boolean,default=True)
    
    bed_allocations = relationship("BedAllocation",back_populates="bed")