# Copyright (c) 2023 Mikheil Tabidze
import logging

from fastapi import Header, HTTPException, Request, status

logger = logging.getLogger().getChild(__name__)


class AuthService:
    def __init__(self, secret_keys: list[str]):
        self._secret_keys = secret_keys

    async def __call__(
        self,
        request: Request,
        secret_key: str = Header(
            default=None,
            title="SECRET-KEY",
            description="A secret key header",
            examples=[
                "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
            ],
        ),
    ):
        """The API secret key verification function"""
        if secret_key is None:
            logger.error(f"A secret key header is missing: {request.headers.keys()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        if secret_key not in self._secret_keys:
            logger.error(f"Invalid secret key: {secret_key}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
