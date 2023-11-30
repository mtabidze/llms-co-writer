# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.configs.app_config import Settings
from app.dependencies import get_openai_client
from app.main import create_app
from tests import test_configs


def mock_get_openai_client():
    choice = Mock()
    choice.message.content = "openai content"
    chat_completion = Mock()
    chat_completion.choices = [choice]
    openai_client = Mock()
    openai_client.generate_chat_completion = Mock(return_value=chat_completion)
    return openai_client


@pytest.fixture(scope="session")
def test_client(request) -> TestClient:
    if hasattr(request, "param"):
        param_value = request.param
    else:
        param_value = test_configs.default
    settings = Settings.model_validate(param_value)
    app = create_app(settings=settings)
    app.dependency_overrides[get_openai_client] = mock_get_openai_client
    test_client = TestClient(app)
    return test_client
