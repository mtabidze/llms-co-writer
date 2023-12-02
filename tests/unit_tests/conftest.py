# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import Mock

import pytest


@pytest.fixture(scope="function")
def mock_bling_client(request):
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = None
    bling_client = Mock()
    bling_client.generate_response.return_value = param_value
    return bling_client


@pytest.fixture(scope="function")
def mock_openai_client(request):
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = None
    choice = Mock()
    choice.message.content = param_value
    chat_completion = Mock()
    chat_completion.choices = [choice]
    openai_client = Mock()
    openai_client.generate_chat_completion.return_value = chat_completion
    return openai_client


@pytest.fixture(scope="function")
def mock_redis_client(request):
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = None
    redis_client = Mock()
    redis_client.get_cache_key.return_value = "key"
    redis_client.set.return_value = True
    redis_client.get.return_value = param_value
    return redis_client


@pytest.fixture(scope="function")
def mock_dynamodb_client():
    dynamodb_client = Mock()
    return dynamodb_client


@pytest.fixture(scope="function")
def mock_request():
    request = Mock()
    return request
