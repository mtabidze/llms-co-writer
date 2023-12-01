# Copyright (c) 2023 Mikheil Tabidze
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.configs.app_config import Settings
from app.routers import app_router
from app.services.auth_service import AuthService
from app.services.bling_client import BlingClient, BlingClientError
from app.services.dynamodb_client import DynamodbClient, DynamodbClientError
from app.services.openai_client import OpenaiClient, OpenaiClientError
from app.services.redis_client import RedisClient, RedisClientError

logger = logging.getLogger().getChild(__name__)


def create_app(settings: Settings = None) -> FastAPI:
    """Loads configuration and initializes the FastAPI application."""
    settings = settings or Settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",  # noqa
    )
    logger.info(f"Logger configured with log level '{settings.log_level}'")

    app = FastAPI(
        title="Large language models (LLMs) Co-Writer",
        summary=(
            "The LLMs Co-Writer API is a powerful RESTful service that "
            "leverages the prowess of large language models (LLMs), such "
            "as OpenAI's GPT, to assist in textual completion, co-writing, "
            "and other creative tasks. "
        ),
        version="1.0.0",
        contact={
            "name": "Mikheil Tabidze",
            "url": "https://github.com/mtabidze",
            "email": "m.tabidze@gmail.com",
        },
        license_info={"name": "Proprietary"},
    )
    logger.info("Application initialized.")

    if settings.local_model_path:
        try:
            bling_client = BlingClient(model_path=settings.local_model_path)
            app.state.bling_client = bling_client
            logger.info("BLING client initialized.")
            bling_client.client_test()
        except BlingClientError:
            app.state.bling_client = None
            logger.warning("BLING client initialise failed.")
    else:
        app.state.bling_client = None
        logger.warning("BLING client configuration is missing.")

    if settings.local_model_path:
        try:
            openai_client = OpenaiClient(
                api_key=settings.openai_api_key, model_name=settings.openai_model
            )
            openai_client.client_test()
            app.state.openai_client = openai_client
            logger.info("OpenAI client initialized.")
            openai_client.client_test()
        except OpenaiClientError:
            app.state.openai_client = None
            logger.warning("OpenAI client initialise failed.")
    else:
        app.state.openai_client = None
        logger.warning("OpenAI client configuration is missing.")

    if settings.redis_dsn is not None:
        try:
            redis_client = RedisClient(
                host=settings.redis_dsn.host,
                port=settings.redis_dsn.port,
                username=settings.redis_dsn.username,
                password=settings.redis_dsn.password,
                expiration_seconds=settings.redis_expiration_seconds,
            )
            app.state.redis_client = redis_client
            logger.info("Redis client initialized.")
            redis_client.client_test()
        except RedisClientError:
            app.state.redis_client = None
            logger.warning("Redis client initialise failed.")
    else:
        app.state.redis_client = None
        logger.warning("Redis configuration is missing.")

    if (
        settings.aws_region is not None
        and settings.aws_access_key_id is not None
        and settings.aws_secret_access_key is not None
        and settings.aws_inferences_table_name is not None
    ):
        try:
            dynamodb_client = DynamodbClient(
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                inferences_table_name=settings.aws_inferences_table_name,
            )
            app.state.dynamodb_client = dynamodb_client
            logger.info("DynamoDB client initialized.")
        except DynamodbClientError:
            app.state.dynamodb_client = None
            logger.warning("DynamoDB client initialise failed.")
    else:
        app.state.dynamodb_client = None
        logger.warning("DynamoDB configuration is missing.")

    auth_service = AuthService(secret_keys=settings.secret_keys)
    app.state.auth_service = auth_service
    logger.info("Auth service initialized.")

    router = app_router.create(auth_service=auth_service)
    app.include_router(router=router)
    logger.info("Application router initialized.")

    app.add_middleware(CORSMiddleware)
    logger.debug("Middlewares initialized.")

    logger.info("Application initialized.")
    return app
