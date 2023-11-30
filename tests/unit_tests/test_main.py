# Copyright (c) 2023 Mikheil Tabidze
from fastapi import FastAPI

from app.configs.app_config import Settings
from app.main import create_app
from tests import test_configs


def test_create_app():
    settings = Settings.model_validate(test_configs.default)
    app = create_app(settings=settings)

    assert isinstance(app, FastAPI)
