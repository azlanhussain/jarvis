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

## Voice Modification History

Jarvis can be modified to operate with voice, and this was already explored in this repo.

Previous working/attempted voice pieces included:

- microphone recording with `sounddevice`
- press-Enter-to-start and press-Enter-to-stop recording
- local speech-to-text with `faster-whisper`
- English-only Whisper transcription via `language="en"`
- OpenAI speech-to-text and text-to-speech before the project was changed to Codex-only
- macOS `say` for spoken output

The original Trillion/Jarvis reference design also allowed a higher-quality external voice stack:

- Deepgram for speech-to-text
- ElevenLabs for text-to-speech and custom voices

That stack is not currently implemented in this repo. Adding it would require Deepgram and ElevenLabs API keys, and it should still keep Codex CLI as the agent brain unless the user explicitly asks to rebuild an independent assistant.

Those voice-input paths were removed from the current app because local transcription was unreliable for the user. The current chosen design is text input only, plus a spoken `Task completed` notification.

If the user asks to add voice again, useful implementation guidance:

- Keep Codex CLI as the brain; do not rebuild an independent Jarvis model provider.
- Reuse the prior architecture: record audio, transcribe to text, then send the transcript to the same Codex handoff path used by typed input.
- Prefer a pluggable transcription backend so the user can choose `faster-whisper`, a shell command, or manual transcript fallback.
- Force English transcription if using Whisper: pass `language="en"`.
- Do not speak full Codex replies unless the user explicitly asks; the current preference is completion-only speech.
- Keep a text-only path available as the default and fallback.

## Commands

Install/update editable package:

```bash
python -m pip install --no-use-pep517 -e .
```

When this repo is cloned or pulled on another machine, the `jarvis` command will not exist until the package is installed there. The other machine also needs Codex CLI installed and logged in, plus macOS `say` for completion speech.

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
