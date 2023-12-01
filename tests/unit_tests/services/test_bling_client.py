# Copyright (c) 2023 Mikheil Tabidze
from unittest.mock import patch

import pytest
from mock.mock import MagicMock, Mock
from torch import tensor

from app.services.bling_client import (
    BlingClient,
    BlingClientInitialisationError,
    ResponseGenerationError,
)

test_attention_mask_tensor = tensor(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
)
test_input_ids_tensor = tensor(
    [
        [
            29,
            13961,
            32056,
            2752,
            1416,
            310,
            378,
            1981,
            13,
            285,
            309,
            717,
            8688,
            1107,
            1711,
            15,
            187,
            1276,
            310,
            619,
            2363,
            32,
            187,
            29,
            12042,
            32056,
        ]
    ]
)

test_model_output_tensor = tensor(
    [
        [
            29,
            13961,
            32056,
            2752,
            1416,
            310,
            378,
            1981,
            13,
            285,
            309,
            717,
            8688,
            1107,
            1711,
            15,
            187,
            1276,
            310,
            619,
            2363,
            32,
            187,
            29,
            12042,
            32056,
            8688,
            1107,
            1711,
            0,
        ]
    ]
)


@patch("app.services.bling_client.AutoModelForCausalLM")
@patch("app.services.bling_client.AutoTokenizer")
def test_init_exception(mock_auto_tokenizer, mock_auto_model_for_causal_lm):
    mock_auto_model_for_causal_lm.from_pretrained.side_effect = ValueError(
        "test exception"
    )
    with pytest.raises(BlingClientInitialisationError):
        BlingClient(model_path="./")

    mock_auto_tokenizer.from_pretrained.side_effect = ValueError("test exception")
    with pytest.raises(BlingClientInitialisationError):
        BlingClient(model_path="./")


@patch("app.services.bling_client.AutoModelForCausalLM")
@patch("app.services.bling_client.AutoTokenizer")
def test_generate_chat_completion(mock_auto_tokenizer, mock_auto_model_for_causal_lm):
    mock_input_ids = MagicMock()
    mock_input_ids.return_value = test_input_ids_tensor
    mock_input_ids.to = Mock()
    mock_inputs = Mock()
    mock_inputs.input_ids = mock_input_ids
    mock_inputs.attention_mask = test_attention_mask_tensor
    mock_tokenizer = Mock()
    mock_tokenizer.return_value = mock_inputs
    mock_tokenizer.decode.return_value = "99 years old"
    mock_auto_tokenizer.from_pretrained.return_value = mock_tokenizer

    mock_model = Mock()
    mock_model.generate.return_value = test_model_output_tensor
    mock_auto_model_for_causal_lm.from_pretrained.return_value = mock_model

    expected_response = "99 years old"

    test_bling_client = BlingClient(model_path="./test_models")

    result = test_bling_client.generate_response(
        context="My name is Bling, and I am 99 years old.", query="What is my age?"
    )

    assert (
        result == expected_response
    ), f"Expected result to be '{expected_response}', but got: {result}"


@patch("app.services.bling_client.AutoModelForCausalLM")
@patch("app.services.bling_client.AutoTokenizer")
def test_generate_response_exception(
    mock_auto_tokenizer, mock_auto_model_for_causal_lm
):
    mock_input_ids = MagicMock()
    mock_input_ids.return_value = test_input_ids_tensor
    mock_input_ids.to = Mock()
    mock_inputs = Mock()
    mock_inputs.input_ids = mock_input_ids
    mock_inputs.attention_mask = test_attention_mask_tensor
    mock_tokenizer = Mock()
    mock_tokenizer.return_value = mock_inputs
    mock_tokenizer.decode.return_value = "99 years old"
    mock_auto_tokenizer.from_pretrained.return_value = mock_tokenizer

    mock_model = Mock()
    mock_model.generate.side_effect = ValueError("test exception")
    mock_auto_model_for_causal_lm.from_pretrained.return_value = mock_model

    test_bling_client = BlingClient(model_path="./test_models")

    with pytest.raises(ResponseGenerationError):
        test_bling_client.generate_response(
            context="My name is Bling, and I am 99 years old.", query="What is my age?"
        )
