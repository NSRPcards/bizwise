# backend/app/routes/business.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.BusinessResponse])
def get_businesses(
    location: str = Query(None), 
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Business)
    if location:
        query = query.filter(models.Business.location.ilike(f"%{location}%"))
    if category:
        query = query.filter(models.Business.category.ilike(f"%{category}%"))
    return query.all()
