import os
import sys
from weather_service import WeatherService
from weather_model import WeatherData

def main():
    
    API_KEY = os.environ.get("WEATHER_API_KEY")
    
    if not API_KEY:
        print("\n❌ Error: WEATHER_API_KEY is not set in your terminal!")
        sys.exit(1)
        
    service = WeatherService(API_KEY)
    
    print("--- Smart Weather CLI Application ---")
    print("(Type 'exit' or 'q' anytime to quit the application)")
    print("-" * 37)
    
    
    while True:
        city = input("\nEnter city name (e.g., Bamako, Sevare, Paris): ").strip()
        
        
        if city.lower() in ['exit', 'q']:
            print("\n👋 Thank you for using Weather CLI. Goodbye!")
            break  
            
        if city:
            raw_data = service.fetch_current_weather(city)
            weather = WeatherData(raw_data)
            print("\n" + weather.display_summary())
            print("-" * 30)  
        else:
            print("Error: City name cannot be empty.")

if __name__ == "__main__":
    main()
