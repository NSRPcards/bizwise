# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)  # city or area
    category = Column(String, nullable=False)

class Area(Base):
    __tablename__ = "areas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    # indices used for BLSI computation (0-1 or 0-100 as noted)
    foot_traffic_index = Column(Float, default=50.0)   # 0-100
    competitor_count = Column(Integer, default=0)
    avg_rent = Column(Float, default=10000.0)
    crime_index = Column(Float, default=0.2)  # 0-1
    growth_index = Column(Float, default=0.5)  # 0-1
    persona_fit = Column(Float, default=0.5)   # 0-1
    badges = Column(Text, default="")
    # optional: store a precomputed blsi for quick use
    blsi = Column(Float, nullable=True)
