from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import business

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(business.router, prefix="/business", tags=["Business"])
