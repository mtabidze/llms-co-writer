# Copyright (c) 2023 Mikheil Tabidze
import hashlib
import json
import logging

import redis

logger = logging.getLogger().getChild(__name__)


class RedisClient:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        expiration_seconds: int,
    ):
        try:
            self._client = redis.Redis(
                host=host,
                port=port,
                username=username,
                password=password,
                decode_responses=True,
            )
        except Exception as e:
            logger.error(f"Failed to initialise Redis client: {e}")
            raise RedisClientInitialisationError from None
        self.expiration_seconds = expiration_seconds

    def client_test(self, key: str = None, value: str = None):
        key = key or "test key"
        value = value or "test value"
        logger.debug(f"Input: {key=} {value=}")
        try:
            self.delete(key=key)
            self.set(key=key, value=value)
            cached_value = self.get(key=key)
            logger.debug(f"Cached value: {cached_value}")
        except Exception as e:
            logger.error(f"Redis client test failed: {e}")
            raise RedisClientTestError from None
        if cached_value != value:
            logger.error(
                f"Redis client test failed: {key=}, {value=}, {cached_value=}."
            )
            raise RedisClientTestError

    def get(self, key: str):
        try:
            return self._client.get(name=key)
        except Exception as e:
            logger.error(f"Failed to get value for {key=} from Redis: {e}")
            raise RedisClientRetrievalError from None

    def set(self, key: str, value, expiration_seconds: int = None):
        try:
            return self._client.set(
                name=key, value=value, ex=expiration_seconds or self.expiration_seconds
            )
        except Exception as e:
            logger.error(f"Failed to set {key=} in Redis: {e}")
            raise RedisClientInsertionError from None

    def delete(self, key: str):
        try:
            return self._client.delete(key)
        except Exception as e:
            logger.error(f"Failed to delete {key=} from Redis: {e}")
            raise RedisClientDeletionError from None

    @staticmethod
    def get_sha256_hash(value):
        json_str = json.dumps(value, sort_keys=True)
        sha256_hash = hashlib.sha256(json_str.encode()).hexdigest()
        return sha256_hash

    @staticmethod
    def get_cache_key(prefix: str, value):
        clean_prefix = prefix.strip().replace(" ", "_")
        sha256_hash = RedisClient.get_sha256_hash(value=value)
        cache_key = f"{clean_prefix}_{sha256_hash}"
        return cache_key


class RedisClientError(Exception):
    """Base exception class for the Redis client module."""

    pass


class RedisClientInitialisationError(RedisClientError):
    """Exception raised when Redis initialization fails."""

    pass


class RedisClientTestError(RedisClientError):
    """Exception raised when Redis test fails."""

    pass


class RedisClientRetrievalError(RedisClientError):
    """Exception raised when Redis retrieval fails."""

    pass


class RedisClientInsertionError(RedisClientError):
    """Exception raised when Redis insertion fails."""

    pass


class RedisClientDeletionError(RedisClientError):
    """Exception raised when Redis deletion fails."""

    pass
