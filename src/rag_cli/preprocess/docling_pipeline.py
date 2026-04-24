from __future__ import annotations

from pathlib import Path


SUPPORTED_EXTS = {"pdf", "docx", "md"}


def collect_files(src: Path, exts: set[str], recursive: bool) -> list[Path]:
    if src.is_file():
        return [src] if src.suffix.lstrip(".").lower() in exts else []
    pattern = "**/*" if recursive else "*"
    return [
        p
        for p in src.glob(pattern)
        if p.is_file() and p.suffix.lstrip(".").lower() in exts
    ]


def to_markdown(file_path: Path) -> str:
    ext = file_path.suffix.lstrip(".").lower()
    if ext == "md":
        return file_path.read_text(encoding="utf-8")

    # Placeholder fallback conversion for binary docs.
    # If docling is available, this can be replaced with real conversion logic.
    return (
        f"# Converted from {file_path.name}\n\n"
        "Docling conversion is not configured in this environment.\n"
        f"Original path: `{file_path}`\n"
    )

