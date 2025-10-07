# backend/app/routes/simulate.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
import math

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# baseline visitors per day by business type multiplier
BUSINESS_BASELINE = {
    "cafe": 120,
    "clinic": 30,
    "grocery": 200,
    "salon": 40,
    "apparel": 60,
    "restaurant": 150,
}

@router.post("/", response_model=schemas.SimulateResponse)
def simulate(req: schemas.SimulateRequest, db: Session = Depends(get_db)):
    area = db.query(models.Area).filter(models.Area.id == req.areaId).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")

    # visitors per day: use provided or estimate from foot_traffic_index
    if req.visitorsPerDay is None:
        baseline = BUSINESS_BASELINE.get(req.__dict__.get("businessType", "").lower(), None)
        # If no businessType supplied in this schema, estimate using foot_traffic_index
        baseline = baseline or 100
        visitors = int((area.foot_traffic_index / 100.0) * baseline)
        visitors = max(1, visitors)
    else:
        visitors = req.visitorsPerDay

    revenueMonthly = visitors * req.daysPerMonth * req.convRate * req.avgSpend
    rent = req.rentOverride if req.rentOverride is not None else area.avg_rent
    costsMonthly = req.staffUtilities + rent
    profitMonthly = revenueMonthly - costsMonthly
    breakEvenMonths = None
    if profitMonthly > 0:
        breakEvenMonths = (req.setupCost / profitMonthly) if profitMonthly > 0 else None
    return {
        "revenueMonthly": round(revenueMonthly, 2),
        "costsMonthly": round(costsMonthly, 2),
        "profitMonthly": round(profitMonthly, 2),
        "breakEvenMonths": round(breakEvenMonths, 2) if breakEvenMonths is not None else None
    }
