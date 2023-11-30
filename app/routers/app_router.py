# Copyright (c) 2023 Mikheil Tabidze
from fastapi import APIRouter

from app.routers.v1 import v1_router
from app.services.auth_service import AuthService


def create(auth_service: AuthService):
    app_router = APIRouter()
    router = v1_router.create(auth_service=auth_service)
    app_router.include_router(router=router)
    return app_router
