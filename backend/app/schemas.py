# backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class BusinessBase(BaseModel):
    name: str
    location: str
    category: str

class BusinessResponse(BusinessBase):
    id: int

    class Config:
        orm_mode = True

class AreaResponse(BaseModel):
    id: int
    name: str
    city: str
    lat: Optional[float]
    lng: Optional[float]
    blsi: Optional[float]
    badges: List[str] = []
    # breakdown optional
    breakdown: Optional[dict] = None

    class Config:
        orm_mode = True

class RecommendationsRequest(BaseModel):
    city: str
    businessType: str
    monthlyBudget: float
    targetPersonas: List[str]
    top: int = 5

class RecommendationResponse(BaseModel):
    areaId: int
    name: str
    lat: Optional[float]
    lng: Optional[float]
    blsi: float
    breakdown: dict
    badges: List[str]

class SimulateRequest(BaseModel):
    areaId: int
    setupCost: float
    avgSpend: float
    convRate: float
    visitorsPerDay: Optional[int] = None
    daysPerMonth: int = 30
    staffUtilities: float = 0.0
    rentOverride: Optional[float] = None

class SimulateResponse(BaseModel):
    revenueMonthly: float
    costsMonthly: float
    profitMonthly: float
    breakEvenMonths: Optional[float]
