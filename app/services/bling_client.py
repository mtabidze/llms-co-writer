# Copyright (c) 2023 Mikheil Tabidze
import logging
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger().getChild(__name__)


class BlingClient:
    def __init__(self, model_path: str):
        try:
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.info(f"Device type is '{self._device}'")
            model_repo_path = Path(model_path).resolve()
            self._tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path=model_repo_path
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_repo_path
            )
            self._model.to(self._device)
        except Exception as e:
            logger.error(f"Failed to initialise BLING client: {e}")
            raise BlingClientInitialisationError from None

    def client_test(self, context: str = None, query: str = None):
        context = context or "My name is Bling, and I am 99 years old."
        query = query or "What is my age?"
        logger.debug(f"Input: {context=} {query=}")
        try:
            response = self.generate_response(context=context, query=query)
            logger.debug(f"Model response: {response}")
        except Exception as e:
            logger.error(f"BLING client test failed: {e}")
            raise BlingClientTestError from None

    def generate_response(self, context: str, query: str):
        try:
            full_prompt = f"<human>: {context}\n{query}\n<bot>:"
            logger.debug(f"Full prompt: {full_prompt}")
            inputs = self._tokenizer(full_prompt, return_tensors="pt")
            start_of_output = len(inputs.input_ids[0])
            logger.debug(f"Inputs: {inputs}")
            input_data = inputs.input_ids.to(self._device)
            logger.debug(f"Input data: {input_data}")
            outputs = self._model.generate(
                input_data,
                eos_token_id=self._tokenizer.eos_token_id,
                pad_token_id=self._tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.3,
                max_new_tokens=100,
            )
            logger.debug(f"Outputs: {outputs}")
            output_only = self._tokenizer.decode(
                outputs[0][start_of_output:], skip_special_tokens=True
            )
            logger.debug(f"Output only: {output_only}")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise ResponseGenerationError from None
        return output_only


class BlingClientError(Exception):
    """Base exception class for the BLING client module."""

    pass


class BlingClientTestError(BlingClientError):
    """Exception raised when BLING test fails."""

    pass


class BlingClientInitialisationError(BlingClientError):
    """Exception raised when BLING client initialization fails."""

    pass


class ResponseGenerationError(BlingClientError):
    """Exception raised when response generation fails."""

    pass
