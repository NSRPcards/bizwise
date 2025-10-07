# backend/app/routes/recommendations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
import math

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def norm(x, minv, maxv):
    if maxv == minv:
        return 0.0
    return (x - minv) / (maxv - minv)

@router.post("/", response_model=List[schemas.RecommendationResponse])
def recommend(req: schemas.RecommendationsRequest, db: Session = Depends(get_db)):
    # Fetch candidate areas in the same city
    areas = db.query(models.Area).filter(models.Area.city.ilike(f"%{req.city}%")).all()
    if not areas:
        raise HTTPException(status_code=404, detail="No areas found for this city")

    # derive normalizers
    comp_counts = [a.competitor_count for a in areas]
    comp_min, comp_max = (min(comp_counts), max(comp_counts)) if comp_counts else (0,1)
    comp_max = max(comp_max, comp_min + 1)

    comp_counts = [a.competitor_count for a in areas]
    comp_min, comp_max = (min(comp_counts), max(comp_counts)) if comp_counts else (0,1)
    opp_vals = [a.foot_traffic_index for a in areas]
    opp_min, opp_max = (min(opp_vals), max(opp_vals)) if opp_vals else (0,100)
    opp_max = max(opp_max, opp_min + 1)

    results = []
    for a in areas:
        # compute normalized complementary_poi_count as placeholder -> use growth_index for demo
        norm_comp = 1.0 - norm(a.competitor_count, comp_min, comp_max)  # competition_inverse
        opp = 0.6*(a.foot_traffic_index/100.0) + 0.4*norm(a.growth_index, 0, 1)  # opportunity
        aff = max(0.0, min(1.0, math.sqrt(max(0.0, req.monthlyBudget / (a.avg_rent + 1e-6)))))
        risk_inv = 1.0 - a.crime_index
        gr = a.growth_index
        # persona fit: if any target persona matches badge -> boost
        pf = a.persona_fit if a.persona_fit is not None else 0.5
        blsi_score = 0.25*opp + 0.20*norm_comp + 0.20*aff + 0.10*risk_inv + 0.15*gr + 0.10*pf
        blsi_score = max(0.0, min(1.0, blsi_score))
        blsi100 = round(100.0 * blsi_score, 2)

        # breakdown
        breakdown = {
            "opportunity": round(opp, 3),
            "competition_inverse": round(norm_comp, 3),
            "affordability": round(aff, 3),
            "risk_inverse": round(risk_inv, 3),
            "growth": round(gr, 3),
            "persona_fit": round(pf, 3)
        }
        badges = a.badges.split(",") if a.badges else []
        results.append({
            "areaId": a.id,
            "name": a.name,
            "lat": a.lat,
            "lng": a.lng,
            "blsi": blsi100,
            "breakdown": breakdown,
            "badges": [b for b in badges if b]
        })

    # sort by blsi desc and return top N
    results_sorted = sorted(results, key=lambda r: r["blsi"], reverse=True)
    return results_sorted[: req.top if req.top and req.top>0 else 5]
