# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import patch

import pytest
from mock.mock import Mock

from app.services.redis_client import (
    RedisClient,
    RedisClientDeletionError,
    RedisClientInitialisationError,
    RedisClientInsertionError,
    RedisClientRetrievalError,
    RedisClientTestError,
)


@pytest.fixture(scope="function")
def test_redis_client() -> RedisClient:
    test_redis_client = RedisClient(
        host="127.0.0.1",
        port=6379,
        username="test_username",
        password="test_password",
        expiration_seconds=3600,
    )
    return test_redis_client


@patch("app.services.redis_client.redis")
def test_init_exception(mock_redis):
    mock_redis.Redis.side_effect = ValueError("test exception")

    with pytest.raises(RedisClientInitialisationError):
        RedisClient(
            host="127.0.0.1",
            port=6379,
            username="test_username",
            password="test_password",
            expiration_seconds=3600,
        )


def test_client_test(test_redis_client: RedisClient):
    test_key = "test key"
    test_value = "test value"
    cached_value = "test value"
    test_redis_client._client.delete = Mock(return_value=1)
    test_redis_client._client.set = Mock(return_value=True)
    test_redis_client._client.get = Mock(return_value=cached_value)

    test_redis_client.client_test(key=test_key, value=test_value)


def test_client_test_exception(test_redis_client: RedisClient):
    cached_value = "invalid value"
    test_redis_client._client.get = Mock(return_value=cached_value)

    with pytest.raises(RedisClientTestError):
        test_redis_client.client_test()

    test_redis_client._client.get = Mock(side_effect=Exception("test exception"))
    with pytest.raises(RedisClientTestError):
        test_redis_client.client_test()

    test_redis_client._client.set = Mock(side_effect=Exception("test exception"))
    with pytest.raises(RedisClientTestError):
        test_redis_client.client_test()

    test_redis_client._client.delete = Mock(side_effect=Exception("test exception"))
    with pytest.raises(RedisClientTestError):
        test_redis_client.client_test()


def test_get(test_redis_client: RedisClient):
    cached_value = "test value"
    test_redis_client._client.get = Mock(return_value=cached_value)
    test_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )

    result = test_redis_client.get(key=test_key)

    assert (
        result == cached_value
    ), f"Expected result to be '{cached_value}', but got: {result}"


def test_get_exception(test_redis_client: RedisClient):
    test_redis_client._client.get = Mock(side_effect=Exception("test exception"))
    test_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )

    with pytest.raises(RedisClientRetrievalError):
        test_redis_client.get(key=test_key)


def test_set(test_redis_client: RedisClient):
    test_redis_client._client.set = Mock(return_value=True)
    test_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )
    test_value = "test value"

    result = test_redis_client.set(key=test_key, value=test_value)

    assert result is True, f"Expected result to be 'True', but got: {result}"


def test_set_exception(test_redis_client: RedisClient):
    test_redis_client._client.set = Mock(side_effect=Exception("test exception"))
    test_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )
    test_value = "test value"

    with pytest.raises(RedisClientInsertionError):
        test_redis_client.set(key=test_key, value=test_value)


def test_delete(test_redis_client: RedisClient):
    test_redis_client._client.delete = Mock(return_value=1)
    test_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )

    result = test_redis_client.delete(key=test_key)

    assert result == 1, f"Expected result to be '1', but got: {result}"


def test_delete_exception(test_redis_client: RedisClient):
    test_redis_client._client.delete = Mock(side_effect=Exception("test exception"))
    test_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )

    with pytest.raises(RedisClientDeletionError):
        test_redis_client.delete(key=test_key)


def test_get_sha256_hash():
    test_value = "test value"
    expected_sha256_hash = (
        "dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )

    result = RedisClient.get_sha256_hash(value=test_value)

    assert (
        result == expected_sha256_hash
    ), f"Expected result to be '{expected_sha256_hash}', but got: {result}"


def test_get_cache_key():
    task_prefix = "test prefix"
    test_value = "test value"
    expected_cache_key = (
        "test_prefix_dfb1d41702818e44beaaafb2b5114c3c64d79697ccda31f8e198e4f7618accce"
    )

    result = RedisClient.get_cache_key(prefix=task_prefix, value=test_value)

    assert (
        result == expected_cache_key
    ), f"Expected result to be '{expected_cache_key}', but got: {result}"
