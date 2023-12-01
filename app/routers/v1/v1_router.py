# Copyright (c) 2023 Mikheil Tabidze
from fastapi import APIRouter, Depends

from app.routers.v1.bling_router import bling_router
from app.routers.v1.health_check_router import health_check_router
from app.routers.v1.openai_router import openai_router
from app.services.auth_service import AuthService


def create(auth_service: AuthService):
    auth_service_dependency = Depends(auth_service)
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(
        router=bling_router, dependencies=[auth_service_dependency]
    )

    v1_router.include_router(
        router=openai_router, dependencies=[auth_service_dependency]
    )
    v1_router.include_router(router=health_check_router)
    return v1_router
