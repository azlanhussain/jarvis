"""Terminal interface for Jarvis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jarvis.codex_client import CodexAgent, CodexConfig, CodexError
from jarvis.config import load_config
from jarvis.notifications import say_task_completed


EXIT_COMMANDS = {"/exit", "/quit", "/q"}


def main() -> int:
    args = _parse_args()
    config = load_config()

    if args.test_notify:
        print("Testing completion notification...")
        if say_task_completed(config.tts_voice):
            print("Notification command completed.")
            return 0
        print("Notification command failed.")
        return 2

    agent = CodexAgent(
        CodexConfig(
            command=config.codex_command,
            sandbox=config.codex_sandbox,
            workdir=Path.cwd(),
            timeout_seconds=config.codex_timeout_seconds,
        )
    )

    print(f"{config.assistant_name} is connected to Codex CLI. Type /exit to quit.")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print("\nInterrupted. Type /exit to quit.")
            continue

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            return 0

        print(f"{config.assistant_name}: ", end="", flush=True)
        try:
            reply = agent.ask(user_input)
        except CodexError as exc:
            print(f"Codex error: {exc}")
            continue
        print(reply, end="", flush=True)
        if config.notify_on_complete and not args.no_notify:
            print("\n[Task completed]", flush=True)
            if not say_task_completed(config.tts_voice):
                print("[Notification failed]", flush=True)
        print()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Jarvis.")
    parser.add_argument("--no-notify", action="store_true", help="Do not say Task completed after Codex replies.")
    parser.add_argument("--test-notify", action="store_true", help="Say Task completed once and exit.")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
