from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import business
from app import models, database

# Create all tables
models.Base.metadata.create_all(bind=database.engine)

# FastAPI app
app = FastAPI(title="BizWise API")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(business.router, prefix="/business", tags=["Business"])
