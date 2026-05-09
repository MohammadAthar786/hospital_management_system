from pydantic import BaseModel 
from typing import Optional 
from uuid import UUID
from datetime import date,datetime

class BedAllocationBase(BaseModel):
    patient_id:UUID 
    bed_id:int
    allocated_at:datetime 
    released_at:Optional[datetime]=None
class BedAllocationCreate(BedAllocationBase):
    pass

class BedSmartAllocationCreate(BaseModel):
    patient_id: UUID
    ward: Optional[str] = None
    bed_type: Optional[str] = None

class BedAllocationUpdate(BaseModel):
    patient_id:Optional[UUID]=None
    bed_id:Optional[int]=None
    released_at:Optional[datetime]=None 
class BedAllocationResponse(BedAllocationBase):
    id:int
    allocated_at:datetime
    
    class Config:
        from_attributes=True
    