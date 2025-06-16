from fastapi import Depends, APIRouter

from app.dependencies import get_city_weather_service
from app.schemas import CityWeatherResponse, CityWeatherRequest
from app.service import CityWeatherService


router = APIRouter()


@router.get("/weather", response_model=CityWeatherResponse)
async def get_weather(
    query_param: CityWeatherRequest = Depends(),
    city_weather_service: CityWeatherService = Depends(get_city_weather_service),
) -> CityWeatherResponse:

    city = query_param.city
    response = await city_weather_service.get_weather_by_city(city)
    return response
