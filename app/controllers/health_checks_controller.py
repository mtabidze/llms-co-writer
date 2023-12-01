# Copyright (c) 2023 Mikheil Tabidze
from fastapi import Request

from app.services.bling_client import BlingClient
from app.services.openai_client import OpenaiClient


def get_health_status(
    request: Request,
    bling_client: BlingClient | None,
    openai_client: OpenaiClient | None,
) -> bool:
    liveness_status = get_liveness_status(
        request=request, bling_client=bling_client, openai_client=openai_client
    )
    readiness_status = get_readiness_status(
        request=request, bling_client=bling_client, openai_client=openai_client
    )
    health_status = liveness_status and readiness_status
    return health_status


def get_liveness_status(
    request: Request,
    bling_client: BlingClient | None,
    openai_client: OpenaiClient | None,
) -> bool:
    return True


def get_readiness_status(
    request: Request,
    bling_client: BlingClient | None,
    openai_client: OpenaiClient | None,
) -> bool:
    if bling_client is not None or openai_client is not None:
        return True
    return False
