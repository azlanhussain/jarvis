# Jarvis Project Spec

## Current Purpose

Jarvis is a local text shell for Codex CLI.

The goal is simple: keep using Codex CLI as the real agent brain, but add a small convenience layer that says `Task completed` when Codex finishes a task.

## Current Flow

```text
User types a task into Jarvis
-> Jarvis sends the task to codex exec
-> Codex CLI handles the work using the user's Codex login
-> Jarvis prints Codex's final response
-> Jarvis says "Task completed" with macOS say
```

## Design Decisions

- Jarvis does not call the OpenAI API directly.
- Jarvis does not use Anthropic.
- Jarvis does not do speech-to-text.
- Jarvis does not speak full Codex replies.
- Jarvis only speaks the completion notification.
- Codex CLI remains responsible for model access, tools, sandboxing, and task execution.

## Code Map

- `jarvis/cli.py` - terminal loop and command-line flags
- `jarvis/codex_client.py` - `codex exec` wrapper
- `jarvis/config.py` - environment settings
- `jarvis/notifications.py` - completion speech via macOS `say`
- `tests/test_codex_shell.py` - unit tests

## Commands

Run Jarvis:

```bash
jarvis
```

Exit:

```text
/exit
/quit
/q
```

Test notification:

```bash
jarvis --test-notify
```

Run without completion speech:

```bash
jarvis --no-notify
```

## Defaults

- `JARVIS_CODEX_COMMAND=codex`
- `JARVIS_CODEX_SANDBOX=read-only`
- `JARVIS_CODEX_TIMEOUT_SECONDS=600`
- `JARVIS_NOTIFY_ON_COMPLETE=true`
- `JARVIS_TTS_VOICE=Samantha`

## Safety Posture

Jarvis does not bypass Codex safety.

Jarvis invokes `codex exec` with the configured sandbox. The default is `read-only`. Any broader file-writing or execution behavior should be controlled through Codex CLI settings, not hidden inside Jarvis.

## Out Of Scope For Now

- Voice input
- Local transcription
- Speaking full answers
- Independent model providers
- Tool registry
- Durable memory
- Proactive reminders
- Background heartbeat
