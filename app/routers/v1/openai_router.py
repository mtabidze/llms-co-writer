# Copyright (c) 2023 Mikheil Tabidze
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers import openai_controller
from app.dependencies import get_dynamodb_client, get_openai_client, get_redis_client
from app.models.openai_models import (
    ChatCompletionCreate,
    ChatCompletionOut,
    TokenizeCreate,
    TokenizeOut,
)
from app.services.dynamodb_client import DynamodbClient
from app.services.openai_client import OpenaiClient, OpenaiClientError
from app.services.redis_client import RedisClient

logger = logging.getLogger().getChild(__name__)


openai_router = APIRouter(prefix="/openai", tags=["OpenAI"])


@openai_router.post(
    path="/chat/completions",
    response_model=ChatCompletionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create chat completions",
)
async def create_chat_completions(
    chat_completion_create: ChatCompletionCreate,
    openai_client: OpenaiClient = Depends(get_openai_client),
    redis_client: RedisClient = Depends(get_redis_client),
    dynamodb_client: DynamodbClient = Depends(get_dynamodb_client),
) -> ChatCompletionOut:
    if openai_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service is unavailable",
        )
    create_data = chat_completion_create.model_dump()
    try:
        message = openai_controller.create_chat_completions(
            create_data=create_data,
            openai_client=openai_client,
            redis_client=redis_client,
            dynamodb_client=dynamodb_client,
        )
    except OpenaiClientError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service is unavailable",
        ) from None
    chat_completion_out = ChatCompletionOut(message=message)
    return chat_completion_out


@openai_router.post(
    path="/tokenize",
    response_model=TokenizeOut,
    status_code=status.HTTP_201_CREATED,
    summary="Tokenize",
)
async def tokenize_text(
    tokenize_create: TokenizeCreate,
    openai_client: OpenaiClient = Depends(get_openai_client),
) -> TokenizeOut:
    if openai_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service is unavailable",
        )
    tokenize_data = tokenize_create.model_dump()
    try:
        tokens = openai_controller.tokenize_text(
            tokenize_data=tokenize_data, openai_client=openai_client
        )
    except OpenaiClientError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service is unavailable",
        ) from None
    tokenize_out = TokenizeOut(tokens=tokens, count=len(tokens))
    return tokenize_out
