from pydantic import BaseModel 
from typing import Optional
from uuid import UUID
from datetime import date,datetime

class BedBase(BaseModel):
    ward:str
    bed_type:str
    bed_number:str
    is_available:bool
    
class BedCreate(BedBase):
    pass
class BedUpdate(BaseModel):
    ward:Optional[str]=None
    bed_type:Optional[str]=None
    bed_number:Optional[str]=None
    is_available:Optional[str]=None
class BedResponse(BedBase):
    id:int    
    class Config:
        from_attributes=True
    
