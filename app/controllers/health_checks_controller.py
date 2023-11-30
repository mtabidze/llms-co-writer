# Copyright (c) 2023 Mikheil Tabidze
from fastapi import Request

from app.services.openai_client import OpenaiClient
from app.services.redis_client import RedisClient


def get_health_status(
    request: Request, openai_client: OpenaiClient, redis_client: RedisClient | None
) -> bool:
    liveness_status = get_liveness_status(
        request=request, openai_client=openai_client, redis_client=redis_client
    )
    readiness_status = get_readiness_status(
        request=request, openai_client=openai_client, redis_client=redis_client
    )
    health_status = liveness_status and readiness_status
    return health_status


def get_liveness_status(
    request: Request, openai_client: OpenaiClient, redis_client: RedisClient | None
) -> bool:
    return True


def get_readiness_status(
    request: Request, openai_client: OpenaiClient, redis_client: RedisClient | None
) -> bool:
    if openai_client:
        return True
    return False
