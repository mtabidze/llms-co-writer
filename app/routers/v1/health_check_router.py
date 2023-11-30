# Copyright (c) 2023 Mikheil Tabidze
import logging

from fastapi import APIRouter, Depends, Request, Response, status

from app.controllers.health_checks_controller import (
    get_health_status,
    get_liveness_status,
    get_readiness_status,
)
from app.dependencies import get_openai_client, get_redis_client
from app.models.health_checks_models import HeathCheck, HeathCheckStatus
from app.services.openai_client import OpenaiClient
from app.services.redis_client import RedisClient

logger = logging.getLogger().getChild(__name__)

health_check_router = APIRouter(
    prefix="/health-check",
    tags=["Health checking"],
    responses={
        200: {"description": "Healthy response"},
        500: {"description": "Unhealthy response"},
    },
)


@health_check_router.get(
    path="/",
    response_model=HeathCheck,
    status_code=status.HTTP_200_OK,
    summary="Heath-check",
    description=(
        "Heath checks verify whether an API is running "
        "and ready to accept incoming requests"
    ),
)
async def health_check(
    request: Request,
    response: Response,
    openai_client: OpenaiClient = Depends(get_openai_client),
    redis_client: RedisClient = Depends(get_redis_client),
):
    if get_health_status(
        request=request, openai_client=openai_client, redis_client=redis_client
    ):
        response.status_code = status.HTTP_200_OK
        return HeathCheck(status=HeathCheckStatus.HEALTHY)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return HeathCheck(status=HeathCheckStatus.UNHEALTHY)


@health_check_router.get(
    path="/liveness/",
    response_model=HeathCheck,
    status_code=status.HTTP_200_OK,
    summary="Liveness",
    description="Liveness checks verify whether an API is running.",
)
async def liveness_check(
    request: Request,
    response: Response,
    openai_client: OpenaiClient = Depends(get_openai_client),
    redis_client: RedisClient = Depends(get_redis_client),
):
    if get_liveness_status(
        request=request, openai_client=openai_client, redis_client=redis_client
    ):
        response.status_code = status.HTTP_200_OK
        return HeathCheck(status=HeathCheckStatus.HEALTHY)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return HeathCheck(status=HeathCheckStatus.UNHEALTHY)


@health_check_router.get(
    path="/readiness",
    response_model=HeathCheck,
    status_code=status.HTTP_200_OK,
    summary="Readiness",
    description=(
        "Readiness checks verify whether an API is ready to accept incoming requests."
    ),
)
async def readiness_check(
    request: Request,
    response: Response,
    openai_client: OpenaiClient = Depends(get_openai_client),
    redis_client: RedisClient = Depends(get_redis_client),
):
    if get_readiness_status(
        request=request, openai_client=openai_client, redis_client=redis_client
    ):
        response.status_code = status.HTTP_200_OK
        return HeathCheck(status=HeathCheckStatus.HEALTHY)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return HeathCheck(status=HeathCheckStatus.UNHEALTHY)
