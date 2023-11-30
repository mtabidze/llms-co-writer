# Copyright (c) 2023 Mikheil Tabidze
from fastapi import Request

from app.services.auth_service import AuthService
from app.services.dynamodb_client import DynamodbClient
from app.services.openai_client import OpenaiClient
from app.services.redis_client import RedisClient


def get_auth_service(request: Request) -> AuthService | None:
    auth_service: AuthService = getattr(request.app.state, "auth_service", None)
    return auth_service


def get_openai_client(request: Request) -> OpenaiClient | None:
    openai_client: OpenaiClient = getattr(request.app.state, "openai_client", None)
    return openai_client


def get_redis_client(request: Request) -> RedisClient | None:
    redis_client: RedisClient = getattr(request.app.state, "redis_client", None)
    return redis_client


def get_dynamodb_client(request: Request) -> DynamodbClient | None:
    dynamodb_client: DynamodbClient = getattr(
        request.app.state, "dynamodb_client", None
    )
    return dynamodb_client
