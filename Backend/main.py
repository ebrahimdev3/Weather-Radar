import os
import sys
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from weather_service import WeatherService
from weather_model import WeatherData

# 1. فحص المتغيرات البيئية قبل الإقلاع لمنع السلوك العشوائي في الإنتاج
API_KEY = os.environ.get("WEATHER_API_KEY")
if not API_KEY:
    print("\n❌ CRITICAL ERROR: WEATHER_API_KEY environment variable is not set!")
    print("Please inject the key into your terminal first.\n")
    sys.exit(1)

app = FastAPI(
    title="Interactive Weather Map API",
    version="1.0.0",
    description="High-performance asynchronous API for map interactions"
)

# 2. حماية وتفعيل سماحية الاتصال للـ Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج الفعلي، استبدلها بنطاق موقعك الثابت
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. تهيئة خدمة الطقس المركزية
weather_service = WeatherService(api_key=API_KEY)

@app.get("/api/weather")
async def get_weather(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    نقطة نهاية تستقبل خطوط الطول والعرض وتضخ بيانات طقس نقية ومحمية للإنتاج.
    """
    raw_data = await weather_service.fetch_weather_by_coords(lat, lon)
    weather = WeatherData(raw_data)
    
    if not weather.is_valid:
        raise HTTPException(
            status_code=404, 
            detail="Weather details could not be found for these boundaries."
        )
        
    return weather.to_dict()
