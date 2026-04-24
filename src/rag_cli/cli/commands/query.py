from __future__ import annotations

from pathlib import Path

from rag_cli.cli.output import emit, fail
from rag_cli.config import load_config
from rag_cli.core.lightrag_engine import LightRAGEngine


def run(workspace: Path, question: str, mode: str, top_k: int, fmt: str) -> None:
    if not question.strip():
        fail("missing_question", "Question cannot be empty.", "", fmt)

    cfg = load_config(workspace)
    if not cfg.index_file.exists():
        fail("missing_index", "Index does not exist. Run init and ingest first.", "", fmt)

    engine = LightRAGEngine(cfg)
    result = engine.query(question=question, mode=mode, top_k=top_k)
    emit(result, fmt)

