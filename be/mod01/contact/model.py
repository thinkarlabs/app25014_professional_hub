import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_contact(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    contact_name:str=Field(...)
    phone_no:str=Field(...)
    email:str=Field(...)
    gender_name:str=Field(...)
    gender_id:str=Field(...)
    user_id:str = Field(...)
    user_name:str = Field(...)
class contactUpdate(BaseModel):
    contact_name: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[str] = None
    gender_name: Optional[str] = None
    gender_id: Optional[str] = None