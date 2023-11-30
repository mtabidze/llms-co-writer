# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import patch

import pytest
from mock.mock import Mock

from app.services.openai_client import (
    ChatCompletionGenerationError,
    OpenaiClient,
    OpenaiClientInitialisationError,
)


@patch("app.services.openai_client.OpenAI")
def test_init_exception(mock_openai):
    mock_openai.side_effect = ValueError("test exception")

    with pytest.raises(OpenaiClientInitialisationError):
        OpenaiClient(api_key="test_openai_api_key", model_name="gpt-4")


@patch("app.services.openai_client.OpenAI")
def test_generate_chat_completion(mock_openai):
    expected_chat_completion = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {"content": "openai content", "role": "assistant"},
            }
        ],
        "created": 1677664795,
        "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
        "model": "gpt-4",
        "object": "chat.completion",
        "usage": {"completion_tokens": 17, "prompt_tokens": 57, "total_tokens": 74},
    }
    mock_openai_client = Mock()
    mock_openai_client.chat.completions.create.return_value = expected_chat_completion
    mock_openai.return_value = mock_openai_client

    test_openai_client = OpenaiClient(api_key="test_openai_api_key", model_name="gpt-4")
    test_chat_messages = [{"content": "user content", "role": "user"}]

    result = test_openai_client.generate_chat_completion(messages=test_chat_messages)

    assert (
        result == expected_chat_completion
    ), f"Expected result to be '{expected_chat_completion}', but got: {result}"


@patch("app.services.openai_client.OpenAI")
def test_generate_chat_completion_exception(mock_openai):
    mock_openai_client = Mock()
    mock_openai_client.chat.completions.create.side_effect = ValueError(
        "test exception"
    )
    mock_openai.return_value = mock_openai_client

    test_openai_client = OpenaiClient(api_key="test_openai_api_key", model_name="gpt-4")
    test_chat_messages = [{"content": "user content", "role": "user"}]

    with pytest.raises(ChatCompletionGenerationError):
        test_openai_client.generate_chat_completion(messages=test_chat_messages)
