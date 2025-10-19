from app.database import engine, Base
from app.models import Area, Business, Rating, UserVisit

Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully!")
