# Copyright (c) 2023 Mikheil Tabidze
import logging

import tiktoken
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

logger = logging.getLogger().getChild(__name__)


class OpenaiClient:
    def __init__(self, api_key: str, model_name: str):
        try:
            self._client = OpenAI(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialise OpenAI client: {e}")
            raise OpenaiClientInitialisationError from None
        self.model_name = model_name

    def client_test(self, messages: list[ChatCompletionMessageParam] = None):
        messages = messages or [{"content": "user content", "role": "user"}]
        logger.debug(f"Input messages: {messages=}")
        try:
            chat_completion = self.generate_chat_completion(messages=messages)
            logger.debug(f"Output chat completion: {chat_completion}")
        except Exception as e:
            logger.error(f"OpenAI client test failed: {e}")
            raise OpenaiClientTestError from None

    def generate_chat_completion(
        self, messages: list[ChatCompletionMessageParam]
    ) -> ChatCompletion:
        try:
            chat_completion = self._client.chat.completions.create(
                model=self.model_name, messages=messages
            )
        except Exception as e:
            logger.error(f"Error generating chat completion: {e}")
            raise ChatCompletionGenerationError from None
        return chat_completion

    def tokenize(self, input_text: str, model_name: str | None = None) -> list[int]:
        model_name = model_name or self.model_name
        try:
            encoding = tiktoken.encoding_for_model(model_name=model_name)
            logger.debug(f"Selected encoding {encoding.name} for model {model_name}")
            tokens = encoding.encode(text=input_text)
        except Exception as e:
            logger.error(f"Error tokenizing text: {e}")
            raise TokenizationError from None
        return tokens


class OpenaiClientError(Exception):
    """Base exception class for the OpenAI client module."""

    pass


class OpenaiClientTestError(OpenaiClientError):
    """Exception raised when OpenAI test fails."""

    pass


class OpenaiClientInitialisationError(OpenaiClientError):
    """Exception raised when OpenAI initialization fails."""

    pass


class ChatCompletionGenerationError(OpenaiClientError):
    """Exception raised when chat completion generation fails."""

    pass


class TokenizationError(OpenaiClientError):
    """Exception raised when tokenization fails."""

    pass
