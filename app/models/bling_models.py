# Copyright (c) 2023 Mikheil Tabidze
from pydantic import BaseModel, Field


class BlingPromptCreate(BaseModel):
    context: str = Field(
        default=...,
        title="text_passage",
        description="Text passage context",
        examples=["My name is Bling, and I am 99 years old."],
    )
    query: str = Field(
        default=...,
        title="query",
        description="Specific question or instruction based on the text passage",
        examples=["What is my age?"],
    )


class BlingResponseOut(BaseModel):
    response: str = Field(
        default=...,
        title="response",
        description="The content of the model output",
        examples=["99 years old"],
    )
