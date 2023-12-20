# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.configs.app_config import Settings
from app.dependencies import (
    get_bling_client,
    get_dynamodb_client,
    get_openai_client,
    get_redis_client,
)
from app.main import create_app
from tests import test_configs


def mock_bling_client():
    response = "bling content"
    bling_client = Mock()
    bling_client.generate_response = Mock(return_value=response)
    return bling_client


def mock_get_openai_client():
    choice = Mock()
    choice.message.content = "openai content"
    chat_completion = Mock()
    chat_completion.choices = [choice]
    openai_client = Mock()
    openai_client.generate_chat_completion = Mock(return_value=chat_completion)
    openai_client.tokenize.return_value = [2323, 1495]
    return openai_client


def mock_get_redis_client():
    redis_client = Mock()
    redis_client.get_cache_key.return_value = "key"
    redis_client.set.return_value = True
    redis_client.get.return_value = None
    return redis_client


def mock_get_dynamodb_client():
    dynamodb_client = Mock()
    return dynamodb_client


@pytest.fixture(scope="session")
def test_client(request) -> TestClient:
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = test_configs.default
    settings = Settings.model_validate(param_value)
    app = create_app(settings=settings)
    app.dependency_overrides[get_bling_client] = mock_bling_client
    app.dependency_overrides[get_openai_client] = mock_get_openai_client
    app.dependency_overrides[get_redis_client] = mock_get_redis_client
    app.dependency_overrides[get_dynamodb_client] = mock_get_dynamodb_client
    test_client = TestClient(app)
    return test_client
