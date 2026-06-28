# Jarvis Repo Guidance

## Project Purpose

Jarvis is a local text shell around Codex CLI.

The app does not call OpenAI or Anthropic APIs directly. Codex CLI is the only agent brain. Jarvis sends each user task to `codex exec`, prints the final response, then uses macOS `say` to announce `Task completed`.

## Current Flow

```text
User types into Jarvis
-> Jarvis calls codex exec
-> Codex CLI handles the task using the user's Codex login
-> Jarvis prints Codex's final response
-> Jarvis says "Task completed"
```

## Code Map

- `jarvis/cli.py` - terminal loop and command-line flags
- `jarvis/codex_client.py` - `codex exec` wrapper
- `jarvis/config.py` - environment settings
- `jarvis/notifications.py` - macOS `say` completion notification
- `tests/test_codex_shell.py` - unit tests

## Important Boundaries

- Do not reintroduce OpenAI API or Anthropic provider code unless explicitly requested.
- Do not reintroduce voice input, transcription, or spoken full replies unless explicitly requested.
- Keep Codex CLI responsible for model access, tools, sandboxing, and task execution.
- Keep Jarvis small: text input, Codex handoff, final response print, completion notification.

## Commands

Install/update editable package:

```bash
python -m pip install --no-use-pep517 -e .
```

Run:

```bash
jarvis
```

Run without completion speech:

```bash
jarvis --no-notify
```

Test completion speech:

```bash
jarvis --test-notify
```

Run tests:

```bash
python -m unittest
```

Compile check:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/jarvis-pycache python -m compileall jarvis tests
```
