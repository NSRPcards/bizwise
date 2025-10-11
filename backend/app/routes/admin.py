from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    # Total visitors (dummy for now, can integrate analytics)
    total_visitors = 123  # replace with real analytics if available

    # Frequently searched business category
    category_count = db.query(models.Business.category, func.count(models.Business.id))\
        .group_by(models.Business.category).all()
    category_count = {cat: count for cat, count in category_count}

    # Frequently searched location
    location_count = db.query(models.Business.location, func.count(models.Business.id))\
        .group_by(models.Business.location).all()
    location_count = {loc: count for loc, count in location_count}

    # Average ratings per area
    ratings = db.query(models.UserRating.area_id, func.avg(models.UserRating.rating))\
        .group_by(models.UserRating.area_id).all()
    ratings_dict = {area_id: avg_rating for area_id, avg_rating in ratings}

    return {
        "total_visitors": total_visitors,
        "category_count": category_count,
        "location_count": location_count,
        "ratings": ratings_dict
    }

@router.get("/top-recommended")
def top_recommended(db: Session = Depends(get_db)):
    areas = db.query(models.Area).order_by(models.Area.blsi.desc()).limit(10).all()
    return [{"id": a.id, "name": a.name, "blsi": a.blsi, "city": a.city} for a in areas]
