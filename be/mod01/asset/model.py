import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_asset(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    type_id:str=Field(...)
    type_name:str  = Field(...)
    title:str = Field(...)
    desc:str  = Field(...)
    purch_date: date = Field(...)
    price:int =Field(...)
    warantydetail:str =Field(...)
    identifier:str =Field(...)
    contact_id:str=Field(...)
    contact_name:str  = Field(...)
    user_id:str = Field(...)
    user_name:str = Field(...)
    
class assetUpdate(BaseModel):
    type_id: Optional[str] = None
    type_name: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    purch_date: Optional[date] = None
    price: Optional[int] = None
    warantydetail: Optional[str] = None
    identifier: Optional[str] = None
    contact_id: Optional[str] = None
    contact_name: Optional[str] = None
