import os
import time
from abc import ABC, abstractmethod

import aioboto3
from dotenv import load_dotenv

from app.constants import CACHE_TTL_MINUTES
from app.constants import DYNAMO_DB_TABLE_NAME
from app.schemas import CityWeatherLog


class BaseCityWeatherLogRepository(ABC):
    @abstractmethod
    async def create_log(self, record: CityWeatherLog) -> None:
        """
        Store a weather log record.
        """

    @abstractmethod
    async def get_recent_log(
        self, city: str, max_age_minutes: int
    ) -> CityWeatherLog | None:
        """
        Retrieve the latest weather log for a city within a given max age (in minutes).
        """


class DynamoDBCityWeatherLogRepository(BaseCityWeatherLogRepository):
    def __init__(self):
        load_dotenv()

        self.table_name = DYNAMO_DB_TABLE_NAME
        self.region_name = os.getenv("AWS_REGION")
        self.aws_service_name = "dynamodb"

    async def create_log(self, record: CityWeatherLog) -> None:

        session = aioboto3.Session()
        async with session.resource(
            self.aws_service_name, region_name=self.region_name
        ) as dynamodb:
            table = await dynamodb.Table(self.table_name)
            await table.put_item(Item=record.model_dump())

    async def get_recent_log(
        self, city: str, max_age_minutes: int = CACHE_TTL_MINUTES
    ) -> CityWeatherLog | None:

        now_ts = int(time.time())
        min_ts = now_ts - max_age_minutes * 60

        session = aioboto3.Session()
        async with session.resource(
            self.aws_service_name, region_name=self.region_name
        ) as dynamodb:
            table = await dynamodb.Table(self.table_name)

            response = await table.query(
                KeyConditionExpression="#city = :city AND #created_at >= :min_ts",
                ExpressionAttributeNames={
                    "#city": "city",
                    "#created_at": "created_at",
                },
                ExpressionAttributeValues={
                    ":city": city,
                    ":min_ts": min_ts,
                },
                ScanIndexForward=False,
                Limit=1,
            )

            items = response.get("Items", [])
            if items:
                return CityWeatherLog(**items[0])
            return None
