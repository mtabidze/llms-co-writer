# Copyright (c) 2023 Mikheil Tabidze
import pytest
from fastapi import HTTPException
from mock.mock import Mock

from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_auth_service_success():
    test_secret_keys = ["test_secret_key_1", "test_secret_key_2"]
    test_auth_service = AuthService(secret_keys=test_secret_keys)
    test_secret_key_header = "test_secret_key_1"

    await test_auth_service(request=Mock(), secret_key=test_secret_key_header)


@pytest.mark.asyncio
async def test_auth_service_no_secret_key_header():
    test_secret_keys = ["test_secret_key_1", "test_secret_key_2"]
    test_auth_service = AuthService(secret_keys=test_secret_keys)

    with pytest.raises(HTTPException):
        await test_auth_service(request=Mock())


@pytest.mark.asyncio
async def test_auth_service_invalid_secret_key():
    test_secret_keys = ["test_secret_key_1", "test_secret_key_2"]
    test_auth_service = AuthService(secret_keys=test_secret_keys)
    test_secret_key_header = "invalid_secret_key_1"

    with pytest.raises(HTTPException):
        await test_auth_service(request=Mock(), secret_key=test_secret_key_header)
