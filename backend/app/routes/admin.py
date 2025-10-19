# backend/app/routes/admin.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import get_db
from sqlalchemy import func
from app.models import Area, Business, Rating, UserVisit

router = APIRouter(prefix="/admin", tags=["Admin"])

# Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")  # hashed password


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    message: str
    success: bool


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(data: AdminLoginRequest):
    """Admin login with hardcoded credentials."""
    if data.username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, data.password):
        return {"message": "Login successful", "success": True}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")



@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):

    # 1️⃣ Most searched cities
    most_searched_cities = (
        db.query(Rating.city_name, func.count(Rating.city_name).label("count"))
        .group_by(Rating.city_name)
        .order_by(func.count(Rating.city_name).desc())
        .limit(5)
        .all()
    )
    most_searched_cities = [{"city": r.city_name, "count": r.count} for r in most_searched_cities]

    # 2️⃣ Most searched business categories
    most_searched_businesses = (
        db.query(Business.category, func.count(Business.category).label("count"))
        .group_by(Business.category)
        .order_by(func.count(Business.category).desc())
        .limit(5)
        .all()
    )
    most_searched_businesses = [{"category": r.category, "count": r.count} for r in most_searched_businesses]

    # 3️⃣ Most rated cities (average rating)
    most_rated_cities = (
        db.query(Rating.city_name, func.avg(Rating.rating).label("rating"))
        .group_by(Rating.city_name)
        .order_by(func.avg(Rating.rating).desc())
        .limit(5)
        .all()
    )
    most_rated_cities = [{"city": r.city_name, "rating": round(r.rating, 2)} for r in most_rated_cities]

    # 4️⃣ Total users
    total_users = db.query(func.count(func.distinct(Rating.user_id))).scalar()

    return {
        "mostSearchedCities": most_searched_cities,
        "mostSearchedBusinesses": most_searched_businesses,
        "mostRatedCities": most_rated_cities,
        "totalUsers": total_users,
    }
    # Most searched cities
    city_counts = (
        db.query(Rating.city_name)
        .with_entities(Rating.city_name, func.count(Rating.city_name).label("count"))
        .group_by(Rating.city_name)
        .order_by(func.count(Rating.city_name).desc())
        .limit(5)
        .all()
    )

    # Most searched business types
    business_counts = (
        db.query(Business.category)
        .with_entities(Business.category, func.count(Business.category).label("count"))
        .group_by(Business.category)
        .order_by(func.count(Business.category).desc())
        .limit(5)
        .all()
    )

    # Most rated cities
    rated_cities = (
        db.query(Rating.city_name)
        .with_entities(Rating.city_name, func.avg(Rating.rating).label("avg_rating"))
        .group_by(Rating.city_name)
        .order_by(func.avg(Rating.rating).desc())
        .limit(5)
        .all()
    )

    # User count
    user_count = db.query(Rating.user_id).distinct().count()

    return {
        "most_searched_cities": [{"city": c[0], "count": c[1]} for c in city_counts],
        "most_searched_businesses": [{"business": b[0], "count": b[1]} for b in business_counts],
        "most_rated_cities": [{"city": r[0], "avg_rating": float(r[1])} for r in rated_cities],
        "user_count": user_count
    }
    
    
@router.get("/user-count")
def get_user_count(db: Session = Depends(get_db)):
    count = db.query(UserVisit).count()
    return {"user_count": count}