import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_category(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    name:str=Field(...)
    user_id:str = Field(...)
    user_name:str = Field(...)

class categoryUpdate(BaseModel):
    name: Optional[str] = None
    
    
    
 
    

