# Copyright (c) 2023 Mikheil Tabidze
from enum import Enum

from pydantic import BaseModel, Field


class HeathCheckStatus(str, Enum):
    HEALTHY = "Healthy"
    UNHEALTHY = "Unhealthy"


class HeathCheck(BaseModel):
    status: HeathCheckStatus = Field(
        default=...,
        title="Status",
        description="Health check status",
        examples=[HeathCheckStatus.HEALTHY, HeathCheckStatus.UNHEALTHY],
    )
