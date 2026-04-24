from __future__ import annotations

from pathlib import Path

from rag_cli.cli.output import emit, fail
from rag_cli.config import load_config
from rag_cli.core.lightrag_engine import LightRAGEngine
from rag_cli.preprocess.docling_pipeline import collect_files, to_markdown


def run(workspace: Path, src: Path, ext: str, recursive: bool, fmt: str) -> None:
    cfg = load_config(workspace)
    if not src.exists():
        fail("missing_source", "Source path does not exist.", str(src), fmt)

    exts = {e.strip().lower() for e in ext.split(",") if e.strip()}
    files = collect_files(src, exts, recursive)
    if not files:
        fail("no_files", "No matching files were found for ingestion.", ext, fmt)

    engine = LightRAGEngine(cfg)
    indexed = []
    for file in files:
        markdown = to_markdown(file)
        engine.insert_markdown(file, markdown)
        indexed.append({"doc": file.name, "source_path": str(file)})

    emit(
        {
            "answer": f"Ingested {len(indexed)} file(s).",
            "snippets": [],
            "meta": {"indexed_count": len(indexed), "indexed": indexed},
        },
        fmt,
    )

