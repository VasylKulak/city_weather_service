import logging
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from app.constants import DYNAMO_DB_TABLE_NAME

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")

logger = logging.getLogger(__name__)


def create_table_if_not_exists():
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
    existing_tables = dynamodb.list_tables().get("TableNames", [])

    if DYNAMO_DB_TABLE_NAME not in existing_tables:
        try:
            dynamodb.create_table(
                TableName=DYNAMO_DB_TABLE_NAME,
                KeySchema=[
                    {"AttributeName": "city", "KeyType": "HASH"},
                    {"AttributeName": "created_at", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "city", "AttributeType": "S"},
                    {"AttributeName": "created_at", "AttributeType": "N"},
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            logger.info(f"Creating table '{DYNAMO_DB_TABLE_NAME}'...")

            waiter = dynamodb.get_waiter("table_exists")
            waiter.wait(TableName=DYNAMO_DB_TABLE_NAME)
            logger.info(f"Table '{DYNAMO_DB_TABLE_NAME}' created successfully.")
        except ClientError as e:
            logger.info("Error creating table:", e)
    else:
        logger.info(f"Table '{DYNAMO_DB_TABLE_NAME}' already exists.")
