# Copyright (c) 2023 Mikheil Tabidze
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    content: str = Field(
        default=...,
        title="content",
        description="The contents of the message",
        examples=["Hello"],
    )
    role: str = Field(
        default=...,
        title="role",
        description="The role of the author of this message",
        examples=["user", "system", "assistant"],
    )


class ChatCompletionCreate(BaseModel):
    chat_messages: list[ChatMessage]


class ChatCompletionOut(BaseModel):
    message: str = Field(
        default=...,
        title="message",
        description="The contents of the completion message",
        examples=["Hello"],
    )
