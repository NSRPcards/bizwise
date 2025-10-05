from app import models, database
from sqlalchemy.orm import Session

# Sample businesses
seed_businesses = [
    {"name": "Cafe Mocha", "location": "Pune", "category": "Cafe"},
    {"name": "Healthy Bites", "location": "Pune", "category": "Restaurant"},
    {"name": "Quick Salon", "location": "Mumbai", "category": "Salon"},
    {"name": "Tech Clinic", "location": "Pune", "category": "Clinic"},
]

def seed_db():
    db: Session = database.SessionLocal()
    try:
        for b in seed_businesses:
            business = models.Business(**b)
            db.add(business)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
    print("Seeded database with sample businesses.")
