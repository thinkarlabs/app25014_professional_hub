import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_account(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    acc_title:str=Field(...)
    acc_type_id: str = Field(...)
    acc_type_name: str = Field(...)    
    balance: float = Field(...)
    

class accountUpdate(BaseModel):
    acc_title: Optional[str] = None
    acc_type_name: Optional[str] = None
    balance: Optional[float] = None
    
 
    

