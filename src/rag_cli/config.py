from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

DEFAULT_CONFIG_NAME = "config.json"
DEFAULT_USER_WORKSPACE_DIR = ".rag-cli-tool"


class AppConfig(BaseModel):
    workspace: Path = Field(default=Path("."))
    poe_api_key: str | None = Field(default=None)
    openai_base_url: str = Field(default="https://api.poe.com/v1")
    llm_model: str = Field(default="gemini-3.1-flash-lite")
    embedding_model: str | None = Field(default=None)

    @property
    def rag_dir(self) -> Path:
        return self.workspace / ".rag"

    @property
    def docs_dir(self) -> Path:
        return self.rag_dir / "docs"

    @property
    def index_file(self) -> Path:
        return self.rag_dir / "index.json"

    @property
    def converted_dir(self) -> Path:
        return self.rag_dir / "converted"


def default_workspace() -> Path:
    # Respect HOME env var for test compatibility (Path.home() may ignore it on Windows).
    home = os.getenv("HOME")
    if home:
        return Path(home) / DEFAULT_USER_WORKSPACE_DIR
    return Path.home() / DEFAULT_USER_WORKSPACE_DIR


def resolve_workspace(workspace: Path | None) -> Path:
    base = workspace if workspace is not None else default_workspace()
    return base.resolve()


def load_config(workspace: Path | None) -> AppConfig:
    load_dotenv()
    workspace = resolve_workspace(workspace)
    cfg_path = workspace / ".rag" / DEFAULT_CONFIG_NAME
    file_data: dict[str, Any] = {}
    if cfg_path.exists():
        file_data = json.loads(cfg_path.read_text(encoding="utf-8"))

    env_data: dict[str, Any] = {
        # Prefer POE_API_KEY, but keep OPENAI_API_KEY as backward-compatible fallback.
        "poe_api_key": os.getenv("POE_API_KEY") or os.getenv("OPENAI_API_KEY"),
        "openai_base_url": os.getenv("OPENAI_BASE_URL"),
        "llm_model": os.getenv("LLM_MODEL"),
        "embedding_model": os.getenv("EMBEDDING_MODEL") or None,
    }
    data = {**file_data, **{k: v for k, v in env_data.items() if v}}
    data["workspace"] = workspace
    return AppConfig.model_validate(data)


def save_config(config: AppConfig) -> Path:
    config.rag_dir.mkdir(parents=True, exist_ok=True)
    payload = config.model_dump(mode="json")
    payload["workspace"] = str(config.workspace)
    path = config.rag_dir / DEFAULT_CONFIG_NAME
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path

