from fastapi import APIRouter, HTTPException
from app.schemas import RecommendationsRequest, RecommendationResponse
import os
import httpx

router = APIRouter()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

if not GEOAPIFY_API_KEY:
    print("⚠️ Warning: GEOAPIFY_API_KEY not loaded. Check .env path or variable name.")

BASE_URL = "https://api.geoapify.com/v1/geocode/search"

@router.post("/", response_model=list[RecommendationResponse])
async def get_recommendations(req: RecommendationsRequest):
    try:
        # Step 1: Get coordinates for the city
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(BASE_URL, params={
                "text": req.city,
                "apiKey": GEOAPIFY_API_KEY
            })
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=f"Geoapify error: {resp.text}")

            data = resp.json()
            if not data["features"]:
                raise HTTPException(status_code=404, detail=f"City '{req.city}' not found")

            coords = data["features"][0]["geometry"]["coordinates"]
            lon, lat = coords

        # Step 2: Dummy recommendations
        results = []
        for i in range(req.top):
            results.append(RecommendationResponse(
                areaId=i + 1,
                name=f"{req.businessType.title()} Zone {i+1}",
                lat=lat + (i * 0.01),
                lng=lon + (i * 0.01),
                blsi=75 + i,
                breakdown={"footfall": 1000 + (i * 200), "competition": 10 - i},
                badges=["Top Area"] if i == 0 else ["Emerging"]
            ))

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
