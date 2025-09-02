from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import Optional
from fastapi import Query


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Business
@router.post("/", response_model=schemas.BusinessResponse)
def create_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    db_business = models.Business(
        name=business.name,
        location=business.location,
        category=business.category
    )
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


# Get all businesses with optional filtering
@router.get("/", response_model=list[schemas.BusinessResponse])
def get_businesses(
    location: Optional[str] = Query(None, description="Filter by location"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Business)
    
    if location:
        query = query.filter(models.Business.location.ilike(f"%{location}%"))
    if category:
        query = query.filter(models.Business.category.ilike(f"%{category}%"))
    
    return query.all()

# ✅ Update business
@router.put("/{business_id}", response_model=schemas.BusinessResponse)
def update_business(business_id: int, updated_business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    db_business = db.query(models.Business).filter(models.Business.id == business_id).first()
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    
    db_business.name = updated_business.name
    db_business.location = updated_business.location
    db_business.category = updated_business.category
    
    db.commit()
    db.refresh(db_business)
    return db_business

# ✅ Delete business
@router.delete("/{business_id}")
def delete_business(business_id: int, db: Session = Depends(get_db)):
    db_business = db.query(models.Business).filter(models.Business.id == business_id).first()
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    
    db.delete(db_business)
    db.commit()
    return {"message": "Business deleted successfully"}
