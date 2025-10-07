# backend/app/routes/areas.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.AreaResponse])
def list_areas(db: Session = Depends(get_db)):
    areas = db.query(models.Area).all()
    results = []
    for a in areas:
        badges = a.badges.split(",") if a.badges else []
        results.append({
            "id": a.id,
            "name": a.name,
            "city": a.city,
            "lat": a.lat,
            "lng": a.lng,
            "blsi": a.blsi,
            "badges": [b for b in badges if b],
            "breakdown": None
        })
    return results
