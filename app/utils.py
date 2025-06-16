import time

from app.schemas import CityWeatherResponse


def current_unix_ts() -> int:
    """Return current Unix timestamp as integer."""
    return int(time.time())


def make_log_key(city: str, timestamp: int) -> str:
    """Generate an object storage key for city name and timestamp."""
    return f"{city}_{timestamp}.json"


def normalize_city_name(city: str) -> str:
    return city.strip().lower().replace(" ", "")


def parse_weather_data(data: dict) -> CityWeatherResponse:
    return CityWeatherResponse(
        city=data["name"],
        country=data["sys"]["country"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        description=data["weather"][0]["description"],
        humidity=data["main"]["humidity"],
        pressure=data["main"]["pressure"],
        wind_speed=data["wind"]["speed"],
        clouds=data["clouds"]["all"],
    )
