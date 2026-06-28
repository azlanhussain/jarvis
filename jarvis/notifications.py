"""Small local notification helpers."""

from __future__ import annotations

import subprocess


def say_task_completed(voice: str) -> bool:
    command = ["say"]
    if voice.strip():
        command.extend(["-v", voice.strip()])
    command.append("Task completed")
    completed = subprocess.run(command, check=False)
    return completed.returncode == 0
