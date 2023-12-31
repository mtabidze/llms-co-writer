# Copyright (c) 2023 Mikheil Tabidze
import pytest

from app.controllers import openai_controller


@pytest.mark.parametrize("mock_openai_client", ["openai content"], indirect=True)
def test_create_chat_completions(mock_openai_client):
    create_data = {"chat_messages": [{"content": "user content", "role": "user"}]}

    result = openai_controller.create_chat_completions(
        create_data=create_data,
        openai_client=mock_openai_client,
        redis_client=None,
        dynamodb_client=None,
    )

    mock_openai_client.generate_chat_completion.assert_called_once()
    assert (
        result == "openai content"
    ), f"Expected result from OpenAI client, but got: {result}"


@pytest.mark.parametrize("mock_openai_client", ["openai content"], indirect=True)
@pytest.mark.parametrize("mock_redis_client", ["redis content"], indirect=True)
def test_create_chat_completions_cache_hit(
    mock_openai_client, mock_redis_client, mock_dynamodb_client
):
    create_data = {"chat_messages": [{"content": "user content", "role": "user"}]}

    result = openai_controller.create_chat_completions(
        create_data=create_data,
        openai_client=mock_openai_client,
        redis_client=mock_redis_client,
        dynamodb_client=mock_dynamodb_client,
    )

    mock_openai_client.generate_chat_completion.assert_not_called()
    mock_dynamodb_client.insert_inference.assert_not_called()
    mock_redis_client.get_cache_key.assert_called_once()
    mock_redis_client.get.assert_called_once()
    mock_redis_client.set.assert_not_called()
    assert (
        result == "redis content"
    ), f"Expected result from REDIS client, but got: {result}"


@pytest.mark.parametrize("mock_openai_client", ["openai content"], indirect=True)
@pytest.mark.parametrize("mock_redis_client", [None], indirect=True)
def test_create_cache_miss(mock_openai_client, mock_redis_client, mock_dynamodb_client):
    create_data = {"chat_messages": [{"content": "user content", "role": "user"}]}

    result = openai_controller.create_chat_completions(
        create_data=create_data,
        openai_client=mock_openai_client,
        redis_client=mock_redis_client,
        dynamodb_client=mock_dynamodb_client,
    )

    mock_redis_client.get_cache_key.assert_called_once()
    mock_dynamodb_client.insert_inference.assert_called_once()
    mock_redis_client.get.assert_called_once()
    mock_openai_client.generate_chat_completion.assert_called_once()
    mock_redis_client.set.assert_called_once()
    assert (
        result == "openai content"
    ), f"Expected result from OpenAI client, but got: {result}"


def test_tokenize(mock_openai_client):
    tokenize_data = {"text": "Test text", "model_name": "gpt-4"}
    expected_tokens = [2323, 1495]

    result = openai_controller.tokenize_text(
        tokenize_data=tokenize_data, openai_client=mock_openai_client
    )

    mock_openai_client.tokenize.assert_called_once()
    assert (
        result == expected_tokens
    ), f"Expected result from OpenAI client, but got: {result}"
