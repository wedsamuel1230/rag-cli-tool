from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

from rag_cli.config import AppConfig


@dataclass
class IndexedDoc:
    doc: str
    source_path: str
    section: str
    text: str


class LightRAGEngine:
    """
    Local fallback engine with LightRAG-compatible command behavior.
    This keeps the CLI usable even when external model services are unavailable.
    """

    def __init__(self, config: AppConfig):
        self.config = config
        self.config.rag_dir.mkdir(parents=True, exist_ok=True)
        self.config.docs_dir.mkdir(parents=True, exist_ok=True)
        self.config.converted_dir.mkdir(parents=True, exist_ok=True)
        if not self.config.index_file.exists():
            self._write_index([])

    def _read_index(self) -> list[dict]:
        return json.loads(self.config.index_file.read_text(encoding="utf-8"))

    def _write_index(self, docs: list[dict]) -> None:
        self.config.index_file.write_text(
            json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def insert_markdown(self, file_path: Path, text: str, section: str = "Main") -> None:
        docs = self._read_index()
        docs = [d for d in docs if d["source_path"] != str(file_path)]
        docs.append(
            {
                "doc": file_path.name,
                "source_path": str(file_path),
                "section": section,
                "text": text,
            }
        )
        self._write_index(docs)

    def list_docs(self) -> dict:
        docs = self._read_index()
        return {
            "count": len(docs),
            "docs": [{"doc": d["doc"], "source_path": d["source_path"]} for d in docs],
        }

    def query(self, question: str, mode: str = "hybrid", top_k: int = 3) -> dict:
        started = time.perf_counter()
        docs = self._read_index()
        q_tokens = {t.lower() for t in question.split() if t.strip()}

        def score(item: dict) -> int:
            text = item["text"].lower()
            return sum(1 for tok in q_tokens if tok in text)

        ranked = sorted(docs, key=score, reverse=True)[: max(1, top_k)]
        snippets = [
            {"doc": d["doc"], "section": d.get("section", "Main"), "text": d["text"][:500]}
            for d in ranked
            if score(d) > 0 or not q_tokens
        ]
        if snippets:
            answer = "Found relevant passages in indexed documents."
        else:
            answer = "No strong match found in current index."
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "answer": answer,
            "snippets": snippets,
            "meta": {"mode": mode, "top_k": top_k, "elapsed_ms": elapsed_ms},
        }

