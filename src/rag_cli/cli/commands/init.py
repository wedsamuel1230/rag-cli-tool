from __future__ import annotations

from pathlib import Path

from rag_cli.cli.output import emit
from rag_cli.config import AppConfig, save_config


def run(workspace: Path | None, fmt: str) -> None:
    from rag_cli.config import resolve_workspace
    cfg = AppConfig(workspace=resolve_workspace(workspace))
    cfg.rag_dir.mkdir(parents=True, exist_ok=True)
    cfg.docs_dir.mkdir(parents=True, exist_ok=True)
    cfg.converted_dir.mkdir(parents=True, exist_ok=True)
    cfg.index_file.write_text("[]", encoding="utf-8")
    cfg_path = save_config(cfg)
    emit(
        {
            "answer": "Workspace initialized.",
            "snippets": [],
            "meta": {"workspace": str(workspace.resolve()), "config": str(cfg_path)},
        },
        fmt,
    )

