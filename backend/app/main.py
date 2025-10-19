from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# --- Load environment variables robustly ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
ENV_PATH = os.path.join(BASE_DIR, ".env")

if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env file not found at: {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH)

print("✅ GEOAPIFY_API_KEY loaded as:", os.getenv("GEOAPIFY_API_KEY"))

from app.routes import recommendations, ratings, admin, user_tracking

# --- FastAPI app setup ---
app = FastAPI(title="BizWise Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register routes ---
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(ratings.router)   # ✅ new rating routes
app.include_router(admin.router)
app.include_router(user_tracking.router)

@app.get("/")
def root():
    return {"message": "BizWise backend is running successfully"}
