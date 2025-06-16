from fastapi import Depends

from app import service
from app.clients.object_storage import ObjectStorageClient, S3Client
from app.clients.weather_api import WeatherClient, OpenWeatherMapClient
from app.repository import BaseCityWeatherLogRepository, DynamoDBCityWeatherLogRepository


async def get_weather_api_client() -> WeatherClient:
    return OpenWeatherMapClient()


async def get_object_storage_client() -> ObjectStorageClient:
    return S3Client()


async def get_city_weather_log_repository() -> BaseCityWeatherLogRepository:
    return DynamoDBCityWeatherLogRepository()


async def get_city_weather_service(
    weather_client: WeatherClient = Depends(get_weather_api_client),
    object_storage_client: ObjectStorageClient = Depends(get_object_storage_client),
    city_weather_log_repo: BaseCityWeatherLogRepository = Depends(
        get_city_weather_log_repository
    ),
):
    return service.CityWeatherService(
        weather_client=weather_client,
        object_storage_client=object_storage_client,
        city_weather_log_repo=city_weather_log_repo,
    )
