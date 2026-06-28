import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from weather_service import WeatherService
from weather_model import WeatherData

app = FastAPI(title="Interactive Weather Map API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not API_KEY:
    print(" Error: WEATHER_API_KEY environment variable is not set!")
    sys.exit(1)

weather_service = WeatherService(API_KEY)

@app.get("/api/weather")
async def get_weather(lat: float, lon: float):
    """
    Endpoint that accepts latitude and longitude and returns structural weather JSON data.
    """
    raw_data = weather_service.fetch_weather_by_coords(lat, lon)
    weather = WeatherData(raw_data)
    
    if not weather.is_valid:
        raise HTTPException(status_code=404, detail="Weather data not found for these coordinates.")
        
    return {
        "city": weather.city,
        "temperature": weather.temperature,
        "condition": weather.description.capitalize(),
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed
    }
