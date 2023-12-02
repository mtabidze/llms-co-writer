# Copyright (c) 2023 Mikheil Tabidze
import pytest

from app.controllers import bling_controller


@pytest.mark.parametrize("mock_bling_client", ["bling content"], indirect=True)
def test_create_response(mock_bling_client):
    create_data = {"context": "human context", "query": "human query"}

    result = bling_controller.create_response(
        create_data=create_data,
        bling_client=mock_bling_client,
        redis_client=None,
        dynamodb_client=None,
    )

    mock_bling_client.generate_response.assert_called_once()
    assert (
        result == "bling content"
    ), f"Expected result from BLING client, but got: {result}"


@pytest.mark.parametrize("mock_bling_client", ["bling content"], indirect=True)
@pytest.mark.parametrize("mock_redis_client", ["redis content"], indirect=True)
def test_create_response_cache_hit(
    mock_bling_client, mock_redis_client, mock_dynamodb_client
):
    create_data = {"context": "human context", "query": "human query"}

    result = bling_controller.create_response(
        create_data=create_data,
        bling_client=mock_bling_client,
        redis_client=mock_redis_client,
        dynamodb_client=mock_dynamodb_client,
    )

    mock_bling_client.generate_response.assert_not_called()
    mock_dynamodb_client.insert_inference.assert_not_called()
    mock_redis_client.get_cache_key.assert_called_once()
    mock_redis_client.get.assert_called_once()
    mock_redis_client.set.assert_not_called()
    assert (
        result == "redis content"
    ), f"Expected result from REDIS client, but got: {result}"


@pytest.mark.parametrize("mock_bling_client", ["bling content"], indirect=True)
@pytest.mark.parametrize("mock_redis_client", [None], indirect=True)
def test_create_response_cache_miss(
    mock_bling_client, mock_redis_client, mock_dynamodb_client
):
    create_data = {"context": "human context", "query": "human query"}

    result = bling_controller.create_response(
        create_data=create_data,
        bling_client=mock_bling_client,
        redis_client=mock_redis_client,
        dynamodb_client=mock_dynamodb_client,
    )

    mock_redis_client.get_cache_key.assert_called_once()
    mock_dynamodb_client.insert_inference.assert_called_once()
    mock_redis_client.get.assert_called_once()
    mock_bling_client.generate_response.assert_called_once()
    mock_redis_client.set.assert_called_once()
    assert (
        result == "bling content"
    ), f"Expected result from BLING client, but got: {result}"
