from __future__ import annotations

import json
from typing import Any

import typer


def emit(payload: dict[str, Any], fmt: str) -> None:
    if fmt == "json":
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if "error" in payload:
        err = payload["error"]
        typer.echo(f"Error [{err.get('code', 'unknown')}]: {err.get('message', 'failed')}")
        return
    answer = payload.get("answer")
    if answer:
        typer.echo(answer)
    snippets = payload.get("snippets", [])
    for idx, snip in enumerate(snippets, start=1):
        typer.echo(f"[{idx}] {snip['doc']} ({snip['section']})")
        typer.echo(snip["text"])


def fail(code: str, message: str, details: str = "", fmt: str = "text") -> None:
    payload = {"error": {"code": code, "message": message, "details": details}}
    emit(payload, fmt)
    raise typer.Exit(1)

