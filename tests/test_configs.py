# Copyright (c) 2023 Mikheil Tabidze
default = {
    "log_level": "INFO",
    "openai_api_key": "test_openai_api_key",
    "openai_model": "gpt-4",
    "local_model_path": "ai_models/abc123",
    "redis_dsn": "redis://:@localhost:6379",
    "redis_expiration_seconds": 3600,
    "secret_keys": ["test_secret_key"],
}

no_redis_dsn = {
    "log_level": "INFO",
    "openai_api_key": "test_openai_api_key",
    "openai_model": "gpt-4",
    "redis_expiration_seconds": 3600,
    "secret_keys": ["test_secret_key"],
}

invalid_redis_dsn = {
    "log_level": "INFO",
    "openai_api_key": "test_openai_api_key",
    "openai_model": "gpt-4",
    "redis_dsn": "redis://default:secret@localhost:1234",
    "redis_expiration_seconds": 3600,
    "secret_keys": ["test_secret_key"],
}

invalid_openai_api_key = {
    "log_level": "INFO",
    "openai_api_key": "sk-...",
    "openai_model": "gpt-4",
    "redis_dsn": "redis://:@localhost:6379",
    "redis_expiration_seconds": 3600,
    "secret_keys": ["test_secret_key"],
}
