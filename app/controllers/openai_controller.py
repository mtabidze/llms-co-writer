# Copyright (c) 2023 Mikheil Tabidze
import json
import logging

from app.services.dynamodb_client import DynamodbClient, DynamodbClientInsertionError
from app.services.openai_client import OpenaiClient
from app.services.redis_client import (
    RedisClient,
    RedisClientInsertionError,
    RedisClientRetrievalError,
)

logger = logging.getLogger().getChild(__name__)

SOURCE = "openai"


def create_chat_completions(
    create_data: dict,
    openai_client: OpenaiClient,
    redis_client: RedisClient | None = None,
    dynamodb_client: DynamodbClient | None = None,
) -> str:
    chat_messages = create_data.get("chat_messages")

    cache_key = None
    if redis_client:
        cache_key = redis_client.get_cache_key(prefix=SOURCE, value=chat_messages)
        try:
            cached_value = redis_client.get(key=cache_key)
            if cached_value is not None:
                return cached_value
        except RedisClientRetrievalError:
            pass

    chat_completion = openai_client.generate_chat_completion(messages=chat_messages)
    content = chat_completion.choices[0].message.content

    if redis_client:
        if cache_key is None:
            cache_key = redis_client.get_cache_key(prefix=SOURCE, value=chat_messages)
        try:
            redis_client.set(key=cache_key, value=content)
        except RedisClientInsertionError:
            pass

    if dynamodb_client:
        try:
            dynamodb_client.insert_inference(
                source=SOURCE,
                input_json=json.dumps(chat_messages),
                output_json=chat_completion.model_dump_json(),
            )
        except DynamodbClientInsertionError:
            pass

    return content


def tokenize_text(tokenize_data: dict, openai_client: OpenaiClient) -> list[int]:
    input_text = tokenize_data.get("text")
    model_name = tokenize_data.get("model_name")
    tokens = openai_client.tokenize(input_text=input_text, model_name=model_name)
    return tokens
