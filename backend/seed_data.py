# backend/seed_data.py
from app import models, database
from sqlalchemy.orm import Session

areas_data = [
    {
        "name": "FC Road",
        "city": "Pune",
        "lat": 18.5165,
        "lng": 73.8565,
        "foot_traffic_index": 85.0,
        "competitor_count": 20,
        "avg_rent": 60000,
        "crime_index": 0.08,
        "growth_index": 0.7,
        "persona_fit": 0.75,
        "badges": "student hub,balanced rent,low crime"
    },
    {
        "name": "Koregaon Park",
        "city": "Pune",
        "lat": 18.5355,
        "lng": 73.9030,
        "foot_traffic_index": 72.0,
        "competitor_count": 28,
        "avg_rent": 90000,
        "crime_index": 0.05,
        "growth_index": 0.65,
        "persona_fit": 0.7,
        "badges": "upscale,good nightlife"
    },
    {
        "name": "Camp",
        "city": "Pune",
        "lat": 18.5196,
        "lng": 73.8526,
        "foot_traffic_index": 78.0,
        "competitor_count": 15,
        "avg_rent": 70000,
        "crime_index": 0.12,
        "growth_index": 0.6,
        "persona_fit": 0.6,
        "badges": "business district,high footfall"
    },
    {
        "name": "Viman Nagar",
        "city": "Pune",
        "lat": 18.5603,
        "lng": 73.9143,
        "foot_traffic_index": 68.0,
        "competitor_count": 10,
        "avg_rent": 45000,
        "crime_index": 0.1,
        "growth_index": 0.72,
        "persona_fit": 0.66,
        "badges": "residential,near airport"
    }
]

businesses_data = [
    {"name": "Cafe Mocha", "location": "Pune", "category": "Cafe"},
    {"name": "Health Clinic", "location": "Pune", "category": "Clinic"},
    {"name": "Grocery Hub", "location": "Pune", "category": "Grocery"},
    {"name": "Style Salon", "location": "Pune", "category": "Salon"},
]

def seed():
    db: Session = database.SessionLocal()
    try:
        # clear tables to avoid duplicates
        db.query(models.Business).delete()
        db.query(models.Area).delete()
        db.commit()

        # add areas
        for a in areas_data:
            area = models.Area(
                name=a["name"],
                city=a["city"],
                lat=a["lat"],
                lng=a["lng"],
                foot_traffic_index=a["foot_traffic_index"],
                competitor_count=a["competitor_count"],
                avg_rent=a["avg_rent"],
                crime_index=a["crime_index"],
                growth_index=a["growth_index"],
                persona_fit=a["persona_fit"],
                badges=a["badges"]
            )
            # optional precompute blsi for quick retrieval (not necessary)
            db.add(area)
        db.commit()

        # add businesses
        for b in businesses_data:
            biz = models.Business(name=b["name"], location=b["location"], category=b["category"])
            db.add(biz)
        db.commit()
        print("Seed data added!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
