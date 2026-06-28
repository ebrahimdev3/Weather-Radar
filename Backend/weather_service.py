import requests

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_weather_by_coords(self, lat: float, lon: float) -> dict:
        """
        Fetches current weather data using latitude and longitude.
        Time Complexity: O(1) for a single network API call.
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  
            'lang': 'en'       
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Connection Error: {e}")
            return {}

      