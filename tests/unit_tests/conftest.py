# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import Mock

import pytest


@pytest.fixture(scope="function")
def mock_bling_client(request):
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = None
    response = param_value
    bling_client = Mock()
    bling_client.generate_response = Mock(return_value=response)
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
    openai_client.generate_chat_completion = Mock(return_value=chat_completion)
    return openai_client


@pytest.fixture(scope="function")
def mock_redis_client(request):
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = None
    mock_redis_client = Mock()
    mock_redis_client.get_cache_key = Mock(return_value="key")
    mock_redis_client.get = Mock(return_value=param_value)
    mock_redis_client.set = Mock(return_value=True)
    return mock_redis_client


@pytest.fixture(scope="function")
def mock_request():
    mock_request = Mock()
    return mock_request
