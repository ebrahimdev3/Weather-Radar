class WeatherData:
    def __init__(self, raw_data: dict):
        
        self.is_valid = bool(raw_data and raw_data.get('cod') == 200)
        
        if self.is_valid:
            self.city = raw_data.get('name')
            self.temperature = raw_data['main'].get('temp')
            self.humidity = raw_data['main'].get('humidity')
            self.description = raw_data['weather'][0].get('description')
            self.wind_speed = raw_data['wind'].get('speed')
        else:
            self.city = None
            self.temperature = None
            self.humidity = None
            self.description = None
            self.wind_speed = None

    def display_summary(self) -> str:
        if self.is_valid:
            return (f"🌤️ Weather in {self.city}:\n"
                    f"- Temperature: {self.temperature}°C\n"
                    f"- Condition: {self.description.capitalize()}\n"
                    f"- Humidity: {self.humidity}%\n"
                    f"- Wind Speed: {self.wind_speed} m/s")
        return "❌ Error: Could not retrieve weather data. Please check the city name."
