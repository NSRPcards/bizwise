# backend/app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    category = Column(String, nullable=False)
