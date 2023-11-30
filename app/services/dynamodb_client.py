# Copyright (c) 2023 Mikheil Tabidze
import logging

import boto3

from app.models.inference_records_models import InferenceRecord

logger = logging.getLogger().getChild(__name__)


class DynamodbClient:
    def __init__(
        self,
        region_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        inferences_table_name: str,
    ):
        try:
            dynamodb_resource = boto3.resource(
                service_name="dynamodb",
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            self._inferences_table = dynamodb_resource.Table(inferences_table_name)
        except Exception as e:
            logger.error(f"Failed to initialise DynamoDB client: {e}")
            raise DynamodbClientInitialisationError from None

    def insert_inference(self, source: str, input_json: str, output_json: str):
        inference_record = InferenceRecord(
            source=source, input_json=input_json, output_json=output_json
        )
        try:
            self._inferences_table.put_item(Item=inference_record.model_dump())
        except Exception as e:
            logger.error(f"Failed to put item to DynamoDB: {e}")
            raise DynamodbClientInsertionError from None


class DynamodbClientError(Exception):
    """Base exception class for the DynamoDB client module."""

    pass


class DynamodbClientInitialisationError(DynamodbClientError):
    """Exception raised when DynamoDB initialization fails."""

    pass


class DynamodbClientInsertionError(DynamodbClientError):
    """Exception raised when DynamoDB insertion fails."""

    pass
