import os
import httpx
from typing import Dict, Any, Optional, List
from cachetools import TTLCache

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.geo_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.tile_url = "https://tile.openweathermap.org/map"
        
        self.cache = TTLCache(maxsize=2048, ttl=300)

    async def fetch_weather_by_coords(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        cache_key = (round(lat, 2), round(lon, 2))
        if cache_key in self.cache:
            return self.cache[cache_key]

        params = {'lat': lat, 'lon': lon, 'appid': self.api_key, 'units': 'metric', 'lang': 'en'}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=6.0)
                if response.status_code == 200:
                    data = response.json()
                    self.cache[cache_key] = data
                    return data
                return {}
            except httpx.RequestError:
                return None

    async def search_city_coords(self, city_name: str) -> List[Dict[str, Any]]:
        params = {'q': city_name, 'limit': 1, 'appid': self.api_key}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.geo_url, params=params, timeout=5.0)
                return response.json() if response.status_code == 200 else []
            except httpx.RequestError:
                return []

    async def fetch_map_tile(self, layer: str, z: int, x: int, y: int) -> Optional[bytes]:
        url = f"{self.tile_url}/{layer}/{z}/{x}/{y}.png"
        params = {'appid': self.api_key}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                if response.status_code == 200:
                    return response.content
                return None
            except httpx.RequestError:
                return None
