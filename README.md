# rag-cli-tool

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Packaging](https://img.shields.io/badge/packaging-uv-4B8BBE.svg)](https://github.com/astral-sh/uv)

Production-ready local document RAG CLI with a clean operator workflow for initialize, ingest, query, and index inspection.

Built for teams that want a fast, scriptable command-line retrieval stack with predictable JSON output contracts.

## Features

- `rag-cli init`: bootstrap a reproducible `.rag/` workspace
- `rag-cli ingest`: convert and index PDF, DOCX, and Markdown sources
- `rag-cli query`: run hybrid retrieval and return concise answers with snippets
- `rag-cli docs`: inspect indexed document inventory for debugging and audit
- `--format json`: stable machine-consumable output for automation and agents

## Quickstart

### Agent skills

```bash
npx skills add wedsamuel1230/rag-cli-tool
```

### Manual use

```bash
uv sync
uv run rag-cli --help
uv run rag-cli init --workspace .
uv run rag-cli ingest --src ./docs --recursive --format json
uv run rag-cli query --question "What is SPI timing?" --mode hybrid --format json
```

## Configuration

You can set config via environment variables (or `.env`):

- `POE_API_KEY` (preferred)
- `OPENAI_BASE_URL`
- `LLM_MODEL`
- `EMBEDDING_MODEL` (optional)

Backward compatibility: `OPENAI_API_KEY` is still accepted if `POE_API_KEY` is not set.

### PowerShell machine-level environment setup

```powershell
[Environment]::SetEnvironmentVariable("POE_API_KEY", "your-key", "Machine")
[Environment]::SetEnvironmentVariable("OPENAI_BASE_URL", "https://api.poe.com/v1", "Machine")
[Environment]::SetEnvironmentVariable("LLM_MODEL", "gemini-3.1-flash-lite", "Machine")
# Optional if your provider supports embeddings:
[Environment]::SetEnvironmentVariable("EMBEDDING_MODEL", "", "Machine")
```

Then restart your terminal so new environment values are available to `uv run rag-cli ...`.

### Model notes

- This project no longer defaults to OpenAI models.
- Default API endpoint is `https://api.poe.com/v1`.
- Default LLM is `gemini-3.1-flash-lite` (you can replace it with any supported model).
- `EMBEDDING_MODEL` is optional because some provider catalogs do not expose embedding models in the same list.

The CLI stores local workspace data in `.rag/`:

- `.rag/config.json`
- `.rag/index.json`
- `.rag/converted/`

## Skill definitions

Agent-facing tool descriptors are in `skills/`:

- `skills/search_docs_cli.json`
- `skills/index_files_cli.json`

They use `uv run rag-cli ... --format json` command contracts.

## Development

```bash
uv sync
uv run pytest
```
