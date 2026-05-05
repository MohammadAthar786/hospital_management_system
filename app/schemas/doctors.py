from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

## Base 
class DoctorBase(BaseModel):
    name : str
    specialty: str
    email: EmailStr
    phone :str
## Create 
class DoctorCreate(DoctorBase):
    pass
## Update 
class DoctorUpdate(BaseModel):
    
    name :  Optional[str]=None
    specialty: Optional[str]=None
    email: Optional[EmailStr]=None
    phone :Optional[str]=None
    
## API response  
class DoctorResponse(DoctorBase):
    id:UUID
    created_at: datetime
    
    class Config:
        from_attributes=True