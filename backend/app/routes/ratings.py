# backend/app/routes/ratings.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Rating
from app.database import get_db  # DB session dependency

router = APIRouter(prefix="/ratings", tags=["Ratings"])

# ----------------- Rating Models -----------------
class RatingRequest(BaseModel):
    user_id: str
    city_name: str
    rating: int

class RatingResponse(BaseModel):
    average_rating: float
    count: int

# ----------------- Rating Endpoints -----------------
@router.post("/")
def add_rating(data: RatingRequest, db: Session = Depends(get_db)):
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    new_rating = Rating(user_id=data.user_id, city_name=data.city_name, rating=data.rating)
    db.add(new_rating)
    db.commit()
    return {"message": "Rating saved successfully"}

@router.get("/{city_name}", response_model=RatingResponse)
def get_city_rating(city_name: str, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter_by(city_name=city_name).all()
    if not ratings:
        return {"average_rating": 0, "count": 0}

    avg_rating = sum(r.rating for r in ratings) / len(ratings)
    return {"average_rating": round(avg_rating, 2), "count": len(ratings)}
