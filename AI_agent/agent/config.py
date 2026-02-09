from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


CONFIG_PATH_ENV = 'AI_AGENT_CONFIG'
DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(), 'config.json')


@dataclass
class Config:
    selenium_driver_path: str = ''
    selenium_headless: bool = True
    voice_enabled: bool = False
    tts_enabled: bool = False
    log_level: str = 'INFO'
    openai_api_key: str = ''


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {'1', 'true', 'yes', 'on'}
    return default


def load_config() -> Config:
    path = os.environ.get(CONFIG_PATH_ENV, DEFAULT_CONFIG_PATH)
    data: dict[str, Any] = {}

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    return Config(
        selenium_driver_path=str(data.get('selenium_driver_path', '')).strip(),
        selenium_headless=_as_bool(data.get('selenium_headless', True), True),
        voice_enabled=_as_bool(data.get('voice_enabled', False), False),
        tts_enabled=_as_bool(data.get('tts_enabled', False), False),
        log_level=str(data.get('log_level', 'INFO')).upper(),
        openai_api_key=str(data.get('openai_api_key', '')).strip(),
    )
