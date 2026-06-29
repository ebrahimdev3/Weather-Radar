import os
import sys
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from weather_service import WeatherService
from weather_model import WeatherData

# 🔑 جلب المفتاح تلقائياً بالاسم المعتمد في كودك الحالي
API_KEY = os.environ.get("WEATHER_API_KEY") or os.environ.get("OPENWEATHER_API_KEY")

if not API_KEY:
    print("\n❌ CRITICAL ERROR: Neither WEATHER_API_KEY nor OPENWEATHER_API_KEY environment variable is set!\n")
    sys.exit(1)

app = FastAPI(title="Secure Weather Radar Map Proxy API", version="1.1.0")

# 🌐 تفعيل إعدادات CORS لتوافق كاش المتصفح (IndexedDB)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_service = WeatherService(api_key=API_KEY)

@app.get("/api/weather")
async def get_weather(lat: float, lon: float):
    raw_data = await weather_service.fetch_weather_by_coords(lat, lon)
    if raw_data is None:
        raise HTTPException(status_code=503, detail="Weather provider unreachable.")
    weather = WeatherData(raw_data)
    if not weather.is_valid:
        raise HTTPException(status_code=404, detail= "Weather details not found.")
    return weather.to_dict()

# 🌐 نقطة نهاية البحث الآمن عن المدن
@app.get("/api/search")
async def search_city(q: str = Query(..., min_length=1)):
    geo_data = await weather_service.search_city_coords(q)
    if not geo_data:
        raise HTTPException(status_code=404, detail="City not found or upstream error.")
    
    location = geo_data[0]
    return {
        "name": location.get("name"),
        "country": location.get("country"),
        "lat": location.get("lat"),
        "lon": location.get("lon")
    }

# 🗺️ نقطة نهاية جلب طبقات الخريطة مباشرة وحجب المفتاح دون تخزين محلي (No Disk Cache)
@app.get("/api/tiles/{layer}/{z}/{x}/{y}.png")
async def get_weather_tile(layer: str, z: int, x: int, y: int):
    # التحقق من أن الطبقة المطلوبة مدعومة رسمياً وتصحيح التسميات القادمة من الفرونتيند إن لزم
    allowed_layers = ["temp_new", "precipitation_new", "wind_new"]
    
    # تحويل مرن للتسميات القادمة من الواجهة
    target_layer = layer
    if "precipitation" in layer: target_layer = "precipitation_new"
    elif "wind" in layer: target_layer = "wind_new"
    elif "temp" in layer: target_layer = "temp_new"

    if target_layer not in allowed_layers:
        raise HTTPException(status_code=400, detail="Invalid layer name.")
        
    # جلب البلاطة مباشرة من الخدمة لتمريرها فوراً
    tile_content = await weather_service.fetch_map_tile(target_layer, z, x, y)
    if not tile_content:
        raise HTTPException(status_code=404, detail="Tile image unavailable.")
        
    # إرجاع الصورة مباشرة للمتصفح بصيغة PNG ليقوم المتصفح بكاش الـ IndexedDB بشكل مستقل
    return Response(content=tile_content, media_type="image/png")
