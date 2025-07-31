import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_project(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    project_title : str = Field(...)
    status_name : str = Field(...)
    status_id : str = Field(...)
    
class projectUpdate(BaseModel):
    project_title : Optional[str] = None
    status_name : Optional[str] = None
    status_id : Optional[str] = None

