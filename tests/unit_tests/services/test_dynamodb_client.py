# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import patch

import pytest
from mock.mock import Mock

from app.services.dynamodb_client import (
    DynamodbClient,
    DynamodbClientInitialisationError,
    DynamodbClientInsertionError,
)


@patch("app.services.dynamodb_client.boto3")
def test_init_exception(mock_boto3):
    mock_dynamodb_resource = Mock()
    mock_dynamodb_resource.Table.side_effect = ValueError("test exception")
    mock_boto3.resource.return_value = mock_dynamodb_resource
    with pytest.raises(DynamodbClientInitialisationError):
        DynamodbClient(
            region_name="us-east-1",
            aws_access_key_id="test_AK...",
            aws_secret_access_key="test_aVQ...",
            inferences_table_name="test_inferences",
        )

    mock_boto3.resource.side_effect = ValueError("test exception")
    with pytest.raises(DynamodbClientInitialisationError):
        DynamodbClient(
            region_name="us-east-1",
            aws_access_key_id="test_AK...",
            aws_secret_access_key="test_aVQ...",
            inferences_table_name="test_inferences",
        )


@patch("app.services.dynamodb_client.boto3")
def test_insert_inference(mock_boto3):
    put_item_result = {
        "ResponseMetadata": {
            "RequestId": "R0N55HJJBK1I56MIU5C0SV93FBVV4KQNSO5AEMVJF66Q9ASUAAJG",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "server": "Server",
                "date": "Thu, 30 Nov 2023 00:00:45 GMT",
                "content-type": "application/x-amz-json-1.0",
                "content-length": "2",
                "connection": "keep-alive",
                "x-amzn-requestid": (
                    "R0N55HJJBK1I56MIU5C0SV93FBVV4KQNSO5AEMVJF66Q9ASUAAJG"
                ),
                "x-amz-crc32": "2745614147",
            },
            "RetryAttempts": 0,
        }
    }
    mock_dynamodb_table = Mock()
    mock_dynamodb_table.put_item = Mock(return_value=put_item_result)
    mock_dynamodb_resource = Mock()
    mock_dynamodb_resource.Table.return_value = mock_dynamodb_table
    mock_boto3.resource.return_value = mock_dynamodb_resource

    test_dynamodb_client = DynamodbClient(
        region_name="us-east-1",
        aws_access_key_id="test_AK...",
        aws_secret_access_key="test_aVQ...",
        inferences_table_name="test_inferences",
    )
    test_dynamodb_client.insert_inference(
        source="openai", input_json="'Hi'", output_json="'Hi'"
    )

    mock_dynamodb_table.put_item.assert_called_once()


@patch("app.services.dynamodb_client.boto3")
def test_insert_inference_exception(mock_boto3):
    mock_dynamodb_table = Mock()
    mock_dynamodb_table.put_item.side_effect = ValueError("test exception")
    mock_dynamodb_resource = Mock()
    mock_dynamodb_resource.Table.return_value = mock_dynamodb_table
    mock_boto3.resource.return_value = mock_dynamodb_resource

    test_dynamodb_client = DynamodbClient(
        region_name="us-east-1",
        aws_access_key_id="test_AK...",
        aws_secret_access_key="test_aVQ...",
        inferences_table_name="test_inferences",
    )

    with pytest.raises(DynamodbClientInsertionError):
        test_dynamodb_client.insert_inference(
            source="openai", input_json="'Hi'", output_json="'Hi'"
        )
