# backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Optional

# ------------------ Business ------------------
class BusinessBase(BaseModel):
    name: str
    location: str
    category: str

class BusinessResponse(BusinessBase):
    id: int

    class Config:
        orm_mode = True

# ------------------ Area ------------------
class AreaResponse(BaseModel):
    id: int
    name: str
    city: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    blsi: Optional[float] = 0
    badges: List[str] = []
    breakdown: Optional[Dict] = None

    class Config:
        orm_mode = True

# ------------------ Recommendations ------------------
class RecommendationsRequest(BaseModel):
    city: str
    businessType: str
    monthlyBudget: Optional[float] = 0
    targetPersonas: Optional[List[str]] = []
    top: Optional[int] = 5

class RecommendationResponse(BaseModel):
    areaId: int
    name: str
    lat: float
    lng: float
    blsi: float
    breakdown: Dict
    badges: List[str] = []

# ------------------ Simulation ------------------
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
    breakEvenMonths: Optional[float] = None
