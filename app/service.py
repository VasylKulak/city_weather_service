import logging

from app.clients.object_storage import ObjectStorageClient
from app.clients.weather_api import WeatherClient
from app.constants import CACHE_TTL_MINUTES
from app.repository import BaseCityWeatherLogRepository
from app.schemas import CityWeatherLog, CityWeatherResponse
from app.utils import current_unix_ts, make_log_key, normalize_city_name

logger = logging.getLogger(__name__)


class CityWeatherService:
    """
    Service layer responsible for:
      1. Checking cache (DynamoDB log + S3 object)
      2. Fetching fresh data from external API if cache is missing or expired
      3. Uploading JSON to S3
      4. Logging the event in DynamoDB
    """

    def __init__(
        self,
        weather_client: WeatherClient,
        object_storage_client: ObjectStorageClient,
        city_weather_log_repo: BaseCityWeatherLogRepository,
    ):
        self.weather_client = weather_client
        self.storage_client = object_storage_client
        self.city_weather_log_repo = city_weather_log_repo

    async def get_weather_by_city(self, city: str) -> CityWeatherResponse:
        """
        - Check cache: get most recent log (<= configured TTL)
        - If cache exists, load JSON from S3 and return it
        - Otherwise, call external API, store and log the fresh data
        """
        city = normalize_city_name(city)

        cached_log = await self.city_weather_log_repo.get_recent_log(
            city, max_age_minutes=CACHE_TTL_MINUTES
        )

        if cached_log:
            try:
                cached_weather_data = await self.storage_client.download_json(
                    cached_log.storage_path
                )
                return CityWeatherResponse(**cached_weather_data)
            except Exception as e:
                logger.warning(
                    f"[CityWeatherService] Cache load failed for '{city}': {e}"
                )

        fresh_data = await self.weather_client.fetch_weather_by_city(city)
        fresh_data_dict = fresh_data.model_dump()

        timestamp = current_unix_ts()
        storage_path = make_log_key(city, timestamp)
        await self.storage_client.upload_json(fresh_data_dict, storage_path)

        log_record = CityWeatherLog(
            city=city,
            created_at=timestamp,
            storage_path=storage_path,
        )
        await self.city_weather_log_repo.create_log(log_record)

        return fresh_data
