import json
import logging
import os
from abc import ABC, abstractmethod

import aioboto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ObjectStorageClient(ABC):
    """
    Base abstract class for working with object storages.
    """

    @abstractmethod
    async def upload_json(self, data: dict, key: str) -> None:
        """
        Upload a JSON object to object storage under the specified key.
        """

    @abstractmethod
    async def download_json(self, key: str) -> dict:
        """
        Download a JSON object from object storage using the specified key.
        """


class S3Client(ObjectStorageClient):
    def __init__(self):
        load_dotenv()

        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME not set in environment variables")

        self.region_name = os.getenv("AWS_REGION")
        if not self.region_name:
            raise ValueError("AWS_REGION not set in environment variables")

    async def upload_json(self, data: dict, key: str) -> None:
        """
        Asynchronously uploads a JSON object to S3 under the specified key.
        """
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
        ) as s3:

            try:
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=json.dumps(data),
                    ContentType="application/json",
                )
                logger.info(f"Uploaded JSON to s3://{self.bucket_name}/{key}")

            except ClientError as e:
                logger.error(f"Upload failed for key '{key}': {e}")
                raise

    async def download_json(self, key: str) -> dict:
        """
        Asynchronously downloads a JSON object from S3 using the specified key.
        """
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=self.region_name,
        ) as s3:

            try:
                response = await s3.get_object(Bucket=self.bucket_name, Key=key)
                content = await response["Body"].read()
                logger.info(f"Downloaded JSON from s3://{self.bucket_name}/{key}")
                return json.loads(content.decode("utf-8"))

            except ClientError as e:
                logger.error(f"Download failed for key '{key}': {e}")
                raise
