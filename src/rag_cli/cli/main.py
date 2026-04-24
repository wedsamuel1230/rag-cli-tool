from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from rag_cli.cli.commands import docs, ingest, init, query
from rag_cli.config import resolve_workspace

app = typer.Typer(help="rag-cli: User-friendly local document RAG CLI.")


@app.command("init")
def init_cmd(
    workspace: Optional[Path] = typer.Option(None, "--workspace", help="Project workspace root."),
    format: str = typer.Option("text", "--format", help="Output format: text|json."),
) -> None:
    init.run(workspace=resolve_workspace(workspace), fmt=format)


@app.command("ingest")
def ingest_cmd(
    src: Path = typer.Option(..., "--src", help="Source file or folder to index."),
    workspace: Optional[Path] = typer.Option(None, "--workspace", help="Project workspace root."),
    ext: str = typer.Option("pdf,docx,md", "--ext", help="Comma-separated extensions."),
    recursive: bool = typer.Option(False, "--recursive", help="Search source folders recursively."),
    format: str = typer.Option("text", "--format", help="Output format: text|json."),
) -> None:
    ingest.run(
        workspace=resolve_workspace(workspace),
        src=src,
        ext=ext,
        recursive=recursive,
        fmt=format,
    )


@app.command("query")
def query_cmd(
    question: str = typer.Option(..., "--question", help="Natural language question."),
    workspace: Optional[Path] = typer.Option(None, "--workspace", help="Project workspace root."),
    mode: str = typer.Option("hybrid", "--mode", help="Query mode: naive|local|global|hybrid."),
    top_k: int = typer.Option(3, "--top-k", help="Number of snippets to return."),
    format: str = typer.Option("text", "--format", help="Output format: text|json."),
) -> None:
    query.run(
        workspace=resolve_workspace(workspace),
        question=question,
        mode=mode,
        top_k=top_k,
        fmt=format,
    )


@app.command("docs")
def docs_cmd(
    workspace: Optional[Path] = typer.Option(None, "--workspace", help="Project workspace root."),
    format: str = typer.Option("text", "--format", help="Output format: text|json."),
) -> None:
    docs.run(workspace=resolve_workspace(workspace), fmt=format)


if __name__ == "__main__":
    app()

