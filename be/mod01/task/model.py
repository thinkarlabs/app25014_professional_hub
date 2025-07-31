import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_task(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    owner_id: str = Field(...)
    owner_name: str = Field(...)
    reminder_date: date = Field(...)
    project_id: str = Field(...)
    project_name: str  = Field(...)
    status_id: str = Field(...)
    status_name: str = Field(...)
    
    desc: str = Field(...)

class taskUpdate(BaseModel):
    title: Optional[str]  = None
    owner_name: Optional[str]  = None
    reminder_date : Optional[date]  = None
    project_name:Optional[str]  = None
    status_name: Optional[str]  = None
    desc:Optional[str]  = None