---
name: rag-cli-operator
description: Operates this repository's rag-cli workflow with uv, including workspace initialization, document ingestion, querying, and index inspection. Use when the user asks to run rag-cli, ingest files, query indexed docs, inspect .rag status, troubleshoot non-zero command exits, or integrate agent calls that require --format json output.
---

# rag-cli Operator

## Purpose

Run this project's local RAG workflow safely and consistently using `uv run rag-cli ...`.

## When To Use

Use this skill when requests mention:

- `rag-cli`
- `uv`
- `init`, `ingest`, `query`, or `docs`
- document indexing/search in this repo
- tool-friendly JSON outputs (`--format json`)

## Command Order

Follow this order unless the user asks otherwise:

1. `uv sync`
2. `uv run rag-cli init --workspace <path>`
3. `uv run rag-cli ingest --workspace <path> --src <path> [--recursive] [--ext ...] --format json`
4. `uv run rag-cli query --workspace <path> --question "<question>" --mode hybrid --top-k 3 --format json`
5. `uv run rag-cli docs --workspace <path> --format json`

## Standard Command Templates

```bash
uv sync
uv run rag-cli --help
uv run rag-cli init --workspace .
uv run rag-cli ingest --workspace . --src ./docs --recursive --ext "pdf,docx,md" --format json
uv run rag-cli query --workspace . --question "What is SPI timing?" --mode hybrid --top-k 3 --format json
uv run rag-cli docs --workspace . --format json
```

## Output Contract

Default to `--format json` when output will be consumed by an agent/tool.

Expected success shape:

- `answer: string`
- `snippets: [{ doc, section, text }]`
- `meta: object`

Expected error shape:

- `error: { code, message, details }`

If command output is for humans only, `--format text` is acceptable.

## Workspace And Config Rules

- Always pass `--workspace` explicitly when not operating in repo root.
- `init` creates `.rag/` and baseline config/index state.
- Required environment/config keys:
  - `POE_API_KEY` (preferred)
  - `OPENAI_BASE_URL` (default: `https://api.poe.com/v1`)
  - `LLM_MODEL` (default: `gemini-3.1-flash-lite`)
  - `EMBEDDING_MODEL` (optional)
- Backward compatibility:
  - `OPENAI_API_KEY` is accepted if `POE_API_KEY` is not set.

### PowerShell Machine-Level Env Setup

```powershell
[Environment]::SetEnvironmentVariable("POE_API_KEY", "your-key", "Machine")
[Environment]::SetEnvironmentVariable("OPENAI_BASE_URL", "https://api.poe.com/v1", "Machine")
[Environment]::SetEnvironmentVariable("LLM_MODEL", "gemini-3.1-flash-lite", "Machine")
# Optional if your provider supports embeddings:
[Environment]::SetEnvironmentVariable("EMBEDDING_MODEL", "", "Machine")
```

## Agent Integration Notes

Keep parameter naming aligned with:

- `skills/search_docs_cli.json`
  - `workspace`, `question`, `mode`, `top_k`
- `skills/index_files_cli.json`
  - `workspace`, `path`, `recursive`, `ext`

When mapping tool calls, preserve these names to avoid wrapper drift.

## Troubleshooting

### Missing `.rag` index

Symptoms:

- `docs` or `query` fails with missing index messages.

Action:

1. Run `uv run rag-cli init --workspace <path>`
2. Re-run `ingest`
3. Retry `query` or `docs`

### Empty ingest results

Symptoms:

- `ingest` reports no files found or indexed count is zero.

Action:

1. Check `--src` path exists.
2. Confirm extension filter via `--ext`.
3. Add `--recursive` for nested folders.
4. Re-run ingest with `--format json` and inspect `meta`.

### Missing API/env values

Symptoms:

- model/provider errors when running query pipelines that require remote backends.

Action:

1. Set required env keys.
2. Re-run from same shell/session.
3. Verify with a simple `query` call.

### Non-zero exit code

Action sequence:

1. Re-run same command with `--format json`.
2. Parse `error.code` and `error.message`.
3. Apply minimal fix.
4. Re-run only the failed step, then continue command order.
