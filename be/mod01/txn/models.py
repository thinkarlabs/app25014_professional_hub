import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_txn(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    txntype_name: str = Field(...)
    txntype_id: str = Field(...)
    from_acc_name: str = Field(...)
    from_acc_id: str = Field(...)
    txn_title: str = Field(...)
    txn_date: date = Field(...)
    amt: float = Field(...)
    category_name: str = Field(...)
    category_id: str = Field(...)
    to_acc_name: str = Field(...)
    to_acc_id: str = Field(...)
    user_id:str = Field(...)
    user_name:str = Field(...)

class txnUpdate(BaseModel):
    txntype_name: Optional[str] = None
    from_acc_name: Optional[str] = None
    txn_title: Optional[str] = None
    txn_date: Optional[str] = None
    amt: Optional[float] = None
    category_name: Optional[str] = None
    to_acc_name: Optional[str] = None
 
    

