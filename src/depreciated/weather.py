import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_current_weather(city="Denver", api_key=None):
    """
    Returns weather condition: Clear, Rain, Snow, Clouds, etc.
    """
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenWeatherMap API key.")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["weather"][0]["main"]  # e.g., "Rain", "Clear"
    except Exception as e:
        print(f"Weather API error: {e}")
        return "Unknown"
