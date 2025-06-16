import os
from abc import ABC, abstractmethod

import aiohttp
from dotenv import load_dotenv

from app.schemas import CityWeatherResponse
from app.utils import parse_weather_data
from fastapi import HTTPException


class WeatherClient(ABC):
    """
    Base class for weather.
    """

    @abstractmethod
    async def fetch_weather_by_city(self, city: str) -> CityWeatherResponse:
        """
        Method for receiving weather data.
        """


class OpenWeatherMapClient(WeatherClient):
    """
    Async implementation of WeatherService using OpenWeatherMap API.
    """

    def __init__(self):
        load_dotenv()

        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        self.api_key = os.getenv("OPENWEATHER_MAP_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as environment variable.")

    async def fetch_weather_by_city(self, city: str) -> CityWeatherResponse:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    raw_data = await response.json()
                    return parse_weather_data(raw_data)
                else:
                    error = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Failed to fetch weather: {error}",
                    )
