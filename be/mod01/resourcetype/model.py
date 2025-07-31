import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_resourcetype(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    title:str=Field(...)
    
    
class resourcetypeUpdate(BaseModel):
    title: Optional[str] = None