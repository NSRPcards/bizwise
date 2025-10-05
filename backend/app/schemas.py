# backend/app/schemas.py
from pydantic import BaseModel

class BusinessBase(BaseModel):
    name: str
    location: str
    category: str

class BusinessResponse(BusinessBase):
    id: int

    class Config:
        orm_mode = True
