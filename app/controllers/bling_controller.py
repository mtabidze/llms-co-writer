# Copyright (c) 2023 Mikheil Tabidze
import json
import logging

from app.services.bling_client import BlingClient
from app.services.dynamodb_client import DynamodbClient, DynamodbClientInsertionError
from app.services.redis_client import (
    RedisClient,
    RedisClientInsertionError,
    RedisClientRetrievalError,
)

logger = logging.getLogger().getChild(__name__)

SOURCE = "bling"


def create_response(
    create_data: dict,
    bling_client: BlingClient,
    redis_client: RedisClient | None = None,
    dynamodb_client: DynamodbClient | None = None,
) -> str:
    context = create_data.get("context")
    query = create_data.get("query")

    cache_key = None
    if redis_client:
        cache_key = redis_client.get_cache_key(prefix=SOURCE, value=context + query)
        try:
            cached_value = redis_client.get(key=cache_key)
            if cached_value is not None:
                return cached_value
        except RedisClientRetrievalError:
            pass

    model_response = bling_client.generate_response(context=context, query=query)

    if redis_client:
        if cache_key is None:
            cache_key = redis_client.get_cache_key(prefix=SOURCE, value=context + query)
        try:
            redis_client.set(key=cache_key, value=model_response)
        except RedisClientInsertionError:
            pass

    if dynamodb_client:
        try:
            dynamodb_client.insert_inference(
                source=SOURCE,
                input_json=json.dumps(context + query),
                output_json=json.dumps(model_response),
            )
        except DynamodbClientInsertionError:
            pass

    return model_response
