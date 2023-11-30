# Copyright (c) 2023 Mikheil Tabidze
from fastapi import status
from starlette.testclient import TestClient

from tests.functional_tests.ft_constants import CHAT_COMPLETIONS_EP


def test_create_chat_completions(test_client: TestClient):
    payload = {"chat_messages": [{"content": "user content", "role": "user"}]}
    response = test_client.post(
        url=CHAT_COMPLETIONS_EP, json=payload, headers={"secret-key": "test_secret_key"}
    )
    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    message = response_json.get("message")
    assert (
        message == "openai content"
    ), f"Expected result from OpenAI client, but got: {message}"


def test_create_chat_completions_unauthorized(test_client: TestClient):
    payload = {"chat_messages": [{"content": "user content", "role": "user"}]}
    response = test_client.post(url=CHAT_COMPLETIONS_EP, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
