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


class TokenizeCreate(BaseModel):
    text: str = Field(
        default=...,
        title="text",
        description="Text to tokenize",
        examples=["You can think of tokens as pieces of words."],
    )
    model_name: str | None = Field(
        default=None,
        title="Model name",
        description="OpenAI model name",
        examples=["gpt-4"],
    )


class TokenizeOut(BaseModel):
    tokens: list[int] = Field(
        default=...,
        title="Tokens",
        description="List of token integers",
        examples=[[2675, 649, 1781, 315, 11460, 439, 9863, 315, 4339, 13]],
    )
    count: int = Field(
        default=...,
        title="Count",
        description="Number of tokens",
        examples=[10],
    )
