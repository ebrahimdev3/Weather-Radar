import httpx
from typing import Dict, Any
from cachetools import TTLCache

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        # كاش محلي يتسع لـ 2048 نقطة جغرافية متميزة وينتهي تلقائياً بعد 5 دقائق (300 ثانية)
        self.cache = TTLCache(maxsize=2048, ttl=300)

    async def fetch_weather_by_coords(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        جلب بيانات الطقس عبر الإحداثيات بشكل غير متزامن (Non-blocking).
        Time Complexity: O(1) بفضل التخزين المؤقت الفعال للطلبات المتكررة.
        """
        # تقريب الإحداثيات لخانة عشرية واحدة لتجميع طلبات الخريطة المتقاربة جغرافياً في كاش واحد
        cache_key = (round(lat, 2), round(lon, 2))
        
        if cache_key in self.cache:
            return self.cache[cache_key]

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'en'
        }

        # استخدام العميل غير المتزامن لمنع حظر الـ Event Loop لـ FastAPI
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=6.0)
                if response.status_code == 200:
                    data = response.json()
                    self.cache[cache_key] = data
                    return data
                return {}
            except httpx.RequestError as e:
                print(f"[Service Error] Failed to reach provider: {e}")
                return {}
