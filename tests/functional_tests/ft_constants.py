# Copyright (c) 2023 Mikheil Tabidze
BASE_URL = "http://127.0.0.1:8000/"
V1_EP = BASE_URL + "v1/"
OPEN_AI_EP = V1_EP + "openai/"
CHAT_COMPLETIONS_EP = OPEN_AI_EP + "chat/completions/"
HEALTH_CHECK_EP = V1_EP + "health-check/"
LIVENESS_EP = HEALTH_CHECK_EP + "liveness/"
READINESS_EP = HEALTH_CHECK_EP + "readiness/"
