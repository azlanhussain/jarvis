# Jarvis

Jarvis is a small text shell around Codex CLI. You type tasks into Jarvis, Jarvis sends each task to `codex exec`, prints the final Codex response, and then uses macOS `say` to announce:

```text
Task completed
```

Jarvis does not use the OpenAI API directly. It relies on your existing Codex CLI login.

## What Is In This Project

The runnable app code is in `jarvis/`:

- `jarvis/cli.py` - terminal entry point and text loop
- `jarvis/codex_client.py` - wrapper around `codex exec`
- `jarvis/config.py` - environment-based settings
- `jarvis/notifications.py` - macOS `say` completion notification

Supporting files:

- `setup.py` and `setup.cfg` - install the `jarvis` command
- `.env.example` - optional environment settings
- `tests/` - unit tests for the Codex wrapper and notification helper
- `AGENTS.md` - Codex repo guidance and project design notes

## Setup

Prerequisite: Codex CLI must already work on this machine.

```bash
codex
```

Then install Jarvis:

```bash
cd /Users/adamputra/jarvis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-use-pep517 -e .
```

## Installing On Another Machine

After cloning or pulling this repo on another machine, the source code will be present but the `jarvis` command will not exist until you install the package in that machine's Python environment.

```bash
cd /path/to/jarvis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-use-pep517 -e .
```

That machine also needs:

- Codex CLI installed
- Codex CLI logged in and working
- macOS `say` available for the spoken `Task completed` notification

Then test:

```bash
jarvis --test-notify
jarvis
```

## Run

```bash
jarvis
```

Then type a task:

```text
Reply with exactly: hello from codex
```

Exit with:

```text
/exit
```

Also supported:

```text
/quit
/q
```

## Notification

Jarvis says `Task completed` after each successful Codex response.

Test only the notification:

```bash
jarvis --test-notify
```

Disable notification for a run:

```bash
jarvis --no-notify
```

Optional settings:

```bash
export JARVIS_NOTIFY_ON_COMPLETE=true
export JARVIS_TTS_VOICE=Samantha
```

## Codex Settings

Jarvis runs Codex in read-only sandbox mode by default:

```bash
export JARVIS_CODEX_COMMAND=codex
export JARVIS_CODEX_SANDBOX=read-only
export JARVIS_CODEX_TIMEOUT_SECONDS=600
```

The sandbox value is passed to `codex exec --sandbox`.

## Verify

Run tests:

```bash
python -m unittest
```

Compile check:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/jarvis-pycache python -m compileall jarvis tests
```

Live smoke test:

```bash
printf 'Reply with exactly: codex-ok\n/exit\n' | jarvis --no-notify
```

Expected Codex response:

```text
codex-ok
```

## Current Boundaries

- No voice input.
- No speech transcription.
- No OpenAI or Anthropic API provider code.
- No independent Jarvis agent brain.
- No long-term memory or proactive heartbeat.
- Jarvis is intentionally a wrapper around Codex CLI, not a replacement for Codex.
