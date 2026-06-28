import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from jarvis.codex_client import CodexAgent, CodexConfig, CodexError, run_codex
from jarvis.config import load_config
from jarvis.notifications import say_task_completed


class CodexShellTests(unittest.TestCase):
    def test_agent_builds_prompt_with_history(self) -> None:
        agent = CodexAgent(CodexConfig(command="codex"))
        agent.history = []

        prompt = agent._build_prompt("hello")

        self.assertIn("Jarvis", prompt)
        self.assertIn("Latest user request:", prompt)
        self.assertIn("hello", prompt)

    def test_agent_records_successful_turn(self) -> None:
        agent = CodexAgent(CodexConfig(command="codex"))

        with patch("jarvis.codex_client.run_codex", return_value="done"):
            reply = agent.ask("please help")

        self.assertEqual(reply, "done")
        self.assertEqual(agent.history[0].speaker, "user")
        self.assertEqual(agent.history[1].speaker, "codex")

    def test_run_codex_reads_output_last_message(self) -> None:
        def fake_run(command, cwd, text, stdout, stderr, timeout, check):
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text("final answer")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        with patch("jarvis.codex_client.subprocess.run", side_effect=fake_run):
            reply = run_codex(CodexConfig(command="codex", workdir=Path.cwd()), "hi")

        self.assertEqual(reply, "final answer")

    def test_run_codex_reports_failure(self) -> None:
        def fake_run(command, cwd, text, stdout, stderr, timeout, check):
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="bad things happened")

        with patch("jarvis.codex_client.subprocess.run", side_effect=fake_run):
            with self.assertRaises(CodexError):
                run_codex(CodexConfig(command="codex", workdir=Path.cwd()), "hi")

    def test_config_uses_completion_notification_defaults(self) -> None:
        config = load_config()

        self.assertEqual(config.tts_voice, "Samantha")
        self.assertTrue(config.notify_on_complete)

    def test_say_task_completed_uses_macos_say(self) -> None:
        with patch("jarvis.notifications.subprocess.run") as run:
            run.return_value.returncode = 0
            say_task_completed("Alex")

        run.assert_called_once_with(["say", "-v", "Alex", "Task completed"], check=False)


if __name__ == "__main__":
    unittest.main()
