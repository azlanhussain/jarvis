"""Codex CLI wrapper used as Jarvis's only brain."""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List


class CodexError(Exception):
    """Raised when Codex CLI cannot produce a usable reply."""


@dataclass(frozen=True)
class CodexConfig:
    command: str = "codex"
    sandbox: str = "read-only"
    workdir: Path = Path.cwd()
    timeout_seconds: int = 600


@dataclass(frozen=True)
class Turn:
    speaker: str
    text: str


class CodexAgent:
    def __init__(self, config: CodexConfig) -> None:
        self.config = config
        self.history: List[Turn] = []

    def ask(self, user_input: str) -> str:
        clean_input = user_input.strip()
        if not clean_input:
            return ""

        prompt = self._build_prompt(clean_input)
        reply = run_codex(self.config, prompt)
        self.history.append(Turn("user", clean_input))
        self.history.append(Turn("codex", reply))
        return reply

    def _build_prompt(self, latest_input: str) -> str:
        lines = [
            "You are Codex CLI being operated through a text shell named Jarvis.",
            "Respond to the user's latest request. Keep final spoken replies concise when possible.",
            "If you need to run commands or edit files, use normal Codex judgment and safety.",
            "",
        ]
        if self.history:
            lines.append("Conversation so far:")
            for turn in self.history[-12:]:
                lines.append(f"{turn.speaker}: {turn.text}")
            lines.append("")
        lines.append("Latest user request:")
        lines.append(latest_input)
        return "\n".join(lines)


def run_codex(config: CodexConfig, prompt: str) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as output_file:
        output_path = Path(output_file.name)

    command = [
        config.command,
        "exec",
        "--sandbox",
        config.sandbox,
        "--skip-git-repo-check",
        "--output-last-message",
        str(output_path),
        prompt,
    ]

    try:
        completed = subprocess.run(
            command,
            cwd=str(config.workdir),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=config.timeout_seconds,
            check=False,
        )
    except FileNotFoundError as exc:
        raise CodexError("Could not find the `codex` command. Install or log into Codex CLI first.") from exc
    except subprocess.TimeoutExpired as exc:
        raise CodexError("Codex timed out before finishing.") from exc

    try:
        reply = output_path.read_text().strip()
    except OSError:
        reply = ""
    finally:
        _safe_unlink(output_path)

    if completed.returncode != 0:
        detail = _last_lines(completed.stderr or completed.stdout)
        raise CodexError("Codex CLI failed." + (f" {detail}" if detail else ""))

    if not reply:
        reply = _extract_plain_output(completed.stdout).strip()

    if not reply:
        raise CodexError("Codex finished without a final message.")

    return reply


def _extract_plain_output(output: str) -> str:
    useful: List[str] = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("WARNING:", "ERROR:", "202", "OpenAI Codex", "--------")):
            continue
        if stripped in {"user", "assistant"}:
            continue
        useful.append(stripped)
    return "\n".join(useful)


def _last_lines(text: str, max_lines: int = 6) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines[-max_lines:])


def _safe_unlink(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
