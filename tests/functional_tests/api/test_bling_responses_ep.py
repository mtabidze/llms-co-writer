# Copyright (c) 2023 Mikheil Tabidze
from fastapi import status
from starlette.testclient import TestClient

from tests.functional_tests.ft_constants import BLING_RESPONSES_EP


def test_create_chat_completions(test_client: TestClient):
    payload = {"context": "human context", "query": "human query"}
    response = test_client.post(
        url=BLING_RESPONSES_EP, json=payload, headers={"secret-key": "test_secret_key"}
    )
    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    response = response_json.get("response")
    assert (
        response == "bling content"
    ), f"Expected result from BLING client, but got: {response}"


def test_create_chat_completions_unauthorized(test_client: TestClient):
    payload = {"context": "human context", "query": "human query"}
    response = test_client.post(url=BLING_RESPONSES_EP, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
