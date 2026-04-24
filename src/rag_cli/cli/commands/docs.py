from __future__ import annotations

from pathlib import Path

from rag_cli.cli.output import emit, fail
from rag_cli.config import load_config
from rag_cli.core.lightrag_engine import LightRAGEngine


def run(workspace: Path, fmt: str) -> None:
    cfg = load_config(workspace)
    if not cfg.index_file.exists():
        fail("missing_index", "Index does not exist. Run init and ingest first.", "", fmt)
    engine = LightRAGEngine(cfg)
    stats = engine.list_docs()
    emit({"answer": f"{stats['count']} document(s) indexed.", "snippets": [], "meta": stats}, fmt)

