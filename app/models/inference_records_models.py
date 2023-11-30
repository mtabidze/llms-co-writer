# Copyright (c) 2023 Mikheil Tabidze
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_timestamp() -> int:
    return int(datetime.now().timestamp())


class InferenceRecord(BaseModel):
    source: str
    input_json: str
    output_json: str
    timestamp: int = Field(default_factory=get_timestamp)
    id: str = Field(default_factory=generate_uuid)
