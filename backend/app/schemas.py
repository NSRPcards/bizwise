from pydantic import BaseModel

class BusinessCreate(BaseModel):
    name: str
    location: str
    category: str

class BusinessResponse(BusinessCreate):
    id: int

    class Config:
        orm_mode = True
