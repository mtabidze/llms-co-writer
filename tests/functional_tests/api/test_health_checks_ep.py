# Copyright (c) 2023 Mikheil Tabidze
from fastapi import status
from starlette.testclient import TestClient

from tests.functional_tests.ft_constants import (
    HEALTH_CHECK_EP,
    LIVENESS_EP,
    READINESS_EP,
)


def test_health_check(test_client: TestClient):
    response = test_client.get(url=HEALTH_CHECK_EP)

    assert response.status_code == status.HTTP_200_OK


def test_liveness_check(test_client: TestClient):
    response = test_client.get(url=LIVENESS_EP)

    assert response.status_code == status.HTTP_200_OK


def test_readiness_check(test_client: TestClient):
    response = test_client.get(url=READINESS_EP)

    assert response.status_code == status.HTTP_200_OK
