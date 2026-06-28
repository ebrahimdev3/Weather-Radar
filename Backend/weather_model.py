class WeatherData:
    def __init__(self, raw_data: dict):
        self.is_valid = bool(raw_data and raw_data.get('cod') == 200)
        
        if self.is_valid:
            
            self.city = raw_data.get('name') if raw_data.get('name') else "Open Ocean"
            self.temperature = raw_data['main'].get('temp')
            self.humidity = raw_data['main'].get('humidity')
            self.description = raw_data['weather'][0].get('description')
            self.wind_speed = raw_data['wind'].get('speed')
        else:
            self.city = self.temperature = self.humidity = self.description = self.wind_speed = None
