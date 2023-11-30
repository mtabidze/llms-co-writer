# Copyright (c) 2023 Mikheil Tabidze
from app.controllers import health_checks_controller


def test_check_health(mock_request, mock_openai_client, mock_redis_client):
    health_status = health_checks_controller.get_health_status(
        request=mock_request,
        openai_client=mock_openai_client,
        redis_client=mock_redis_client,
    )

    assert isinstance(health_status, bool)


def test_check_liveness(mock_request, mock_openai_client, mock_redis_client):
    liveness_status = health_checks_controller.get_liveness_status(
        request=mock_request,
        openai_client=mock_openai_client,
        redis_client=mock_redis_client,
    )

    assert isinstance(liveness_status, bool)


def test_check_readiness(mock_request, mock_openai_client, mock_redis_client):
    readiness_status = health_checks_controller.get_readiness_status(
        request=mock_request,
        openai_client=mock_openai_client,
        redis_client=mock_redis_client,
    )

    assert isinstance(readiness_status, bool)
