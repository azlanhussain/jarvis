"""Configuration for the Jarvis assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_ASSISTANT_NAME = "Jarvis"
DEFAULT_CODEX_COMMAND = "codex"
DEFAULT_CODEX_SANDBOX = "read-only"
DEFAULT_CODEX_TIMEOUT_SECONDS = 600
DEFAULT_TTS_VOICE = "Samantha"


@dataclass(frozen=True)
class AppConfig:
    assistant_name: str
    codex_command: str
    codex_sandbox: str
    codex_timeout_seconds: int
    tts_voice: str
    notify_on_complete: bool


def load_config() -> AppConfig:
    """Load config from environment variables."""

    return AppConfig(
        assistant_name=os.environ.get("JARVIS_NAME", DEFAULT_ASSISTANT_NAME),
        codex_command=os.environ.get("JARVIS_CODEX_COMMAND", DEFAULT_CODEX_COMMAND),
        codex_sandbox=os.environ.get("JARVIS_CODEX_SANDBOX", DEFAULT_CODEX_SANDBOX),
        codex_timeout_seconds=_read_int("JARVIS_CODEX_TIMEOUT_SECONDS", DEFAULT_CODEX_TIMEOUT_SECONDS),
        tts_voice=os.environ.get("JARVIS_TTS_VOICE", DEFAULT_TTS_VOICE),
        notify_on_complete=_read_bool("JARVIS_NOTIFY_ON_COMPLETE", True),
    )


def _read_int(name: str, default: int) -> int:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError:
        return default

    if value <= 0:
        return default
    return value


def _read_bool(name: str, default: bool) -> bool:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}
