from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Define Base here
Base = declarative_base()

# Example model
class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, index=True)
    category = Column(String, index=True)
