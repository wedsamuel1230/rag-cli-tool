from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from rag_cli.cli.main import app

runner = CliRunner()


def test_init_ingest_query_docs_json_flow(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "mcu.md").write_text(
        "# SPI Timing\nThe MCU SPI clock supports mode 0 and mode 3.\n", encoding="utf-8"
    )

    init_result = runner.invoke(app, ["init", "--workspace", str(tmp_path), "--format", "json"])
    assert init_result.exit_code == 0
    init_json = json.loads(init_result.stdout)
    assert init_json["answer"] == "Workspace initialized."

    ingest_result = runner.invoke(
        app,
        [
            "ingest",
            "--workspace",
            str(tmp_path),
            "--src",
            str(docs_dir),
            "--recursive",
            "--format",
            "json",
        ],
    )
    assert ingest_result.exit_code == 0
    ingest_json = json.loads(ingest_result.stdout)
    assert ingest_json["meta"]["indexed_count"] == 1

    docs_result = runner.invoke(app, ["docs", "--workspace", str(tmp_path), "--format", "json"])
    assert docs_result.exit_code == 0
    docs_json = json.loads(docs_result.stdout)
    assert docs_json["meta"]["count"] == 1

    query_result = runner.invoke(
        app,
        [
            "query",
            "--workspace",
            str(tmp_path),
            "--question",
            "What does SPI timing support?",
            "--mode",
            "hybrid",
            "--format",
            "json",
        ],
    )
    assert query_result.exit_code == 0
    query_json = json.loads(query_result.stdout)
    assert "answer" in query_json
    assert "snippets" in query_json
    assert "meta" in query_json
    assert query_json["meta"]["mode"] == "hybrid"

