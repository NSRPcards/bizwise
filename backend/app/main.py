# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import business, areas, recommendations, simulate
from app import models, database

# ensure tables exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="BizWise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev; restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(business.router, prefix="/business", tags=["Business"])
app.include_router(areas.router, prefix="/areas", tags=["Areas"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(simulate.router, prefix="/simulate", tags=["Simulate"])

@app.get("/")
def root():
    return {"message": "BizWise API running"}
