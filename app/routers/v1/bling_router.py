# Copyright (c) 2023 Mikheil Tabidze
import logging

from fastapi import APIRouter, Depends, status

from app.controllers import bling_controller
from app.dependencies import get_bling_client, get_dynamodb_client, get_redis_client
from app.models.bling_models import BlingPromptCreate, BlingResponseOut
from app.services.bling_client import BlingClient
from app.services.dynamodb_client import DynamodbClient
from app.services.redis_client import RedisClient

logger = logging.getLogger().getChild(__name__)


bling_router = APIRouter(prefix="/bling", tags=["BLING"])


@bling_router.post(
    path="/responses",
    response_model=BlingResponseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create model response",
)
async def create_model_response(
    bling_prompt_create: BlingPromptCreate,
    bling_client: BlingClient = Depends(get_bling_client),
    redis_client: RedisClient = Depends(get_redis_client),
    dynamodb_client: DynamodbClient = Depends(get_dynamodb_client),
) -> BlingResponseOut:
    create_data = bling_prompt_create.model_dump()
    model_response = bling_controller.create_response(
        create_data=create_data,
        bling_client=bling_client,
        redis_client=redis_client,
        dynamodb_client=dynamodb_client,
    )
    bling_response_out = BlingResponseOut(response=model_response)
    return bling_response_out
