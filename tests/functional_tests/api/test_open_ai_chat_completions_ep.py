# Copyright (c) 2023 Mikheil Tabidze
from fastapi import status
from starlette.testclient import TestClient

from tests.functional_tests.ft_constants import (
    OPEN_AI_CHAT_COMPLETIONS_EP,
    OPEN_AI_TOKENIZE_EP,
)


def test_create_chat_completions(test_client: TestClient):
    payload = {"chat_messages": [{"content": "user content", "role": "user"}]}
    response = test_client.post(
        url=OPEN_AI_CHAT_COMPLETIONS_EP,
        json=payload,
        headers={"secret-key": "test_secret_key"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    message = response_json.get("message")
    assert (
        message == "openai content"
    ), f"Expected result from OpenAI client, but got: {message}"


def test_create_chat_completions_unauthorized(test_client: TestClient):
    payload = {"chat_messages": [{"content": "user content", "role": "user"}]}
    response = test_client.post(url=OPEN_AI_CHAT_COMPLETIONS_EP, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    payload = {"chat_messages": [{"content": "user content", "role": "user"}]}
    response = test_client.post(
        url=OPEN_AI_CHAT_COMPLETIONS_EP, json=payload, headers={"secret-key": "abc123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_tokenize(test_client: TestClient):
    expected_tokens = [2323, 1495]
    payload = {"text": "Test text", "model_name": "gpt-4"}
    response = test_client.post(
        url=OPEN_AI_TOKENIZE_EP,
        json=payload,
        headers={"secret-key": "test_secret_key"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    tokens = response_json.get("tokens")
    assert (
        tokens == expected_tokens
    ), f"Expected result from OpenAI client, but got: {tokens}"


def test_tokenize_unauthorized(test_client: TestClient):
    payload = {"text": "Test text", "model_name": "gpt-4"}
    response = test_client.post(url=OPEN_AI_TOKENIZE_EP, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    payload = {"chat_messages": [{"content": "user content", "role": "user"}]}
    response = test_client.post(
        url=OPEN_AI_TOKENIZE_EP, json=payload, headers={"secret-key": "abc123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
