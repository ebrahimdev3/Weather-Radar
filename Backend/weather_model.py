class WeatherData:
    
    def __init__(self, raw_data: dict):
        
        self.is_valid = bool(raw_data and str(raw_data.get('cod')) == '200')
        
        if self.is_valid:
            
            self.city = raw_data.get('name') if raw_data.get('name') else "Open Ocean"
            self.temperature = raw_data.get('main', {}).get('temp')
            self.humidity = raw_data.get('main', {}).get('humidity')
            self.wind_speed = raw_data.get('wind', {}).get('speed')
            
            weather_list = raw_data.get('weather', [{}])
            self.description = weather_list[0].get('description', 'No description available')
        else:
            self.city = self.temperature = self.humidity = self.description = self.wind_speed = None

    def to_dict(self) -> dict:
        return {
            "city": self.city,
            "temperature": self.temperature,
            "condition": self.description.capitalize() if self.description else None,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed
        }
