# Changelog

## [0.2.0] - 2026-04-25

### Added
- Global install support via `uv tool install rag-cli-tool[rag,doc]`
- Default workspace resolution (`~/.rag-cli-tool` when `--workspace` omitted)
- Cross-platform user-profile workspace for global installs

### Changed
- Renamed CLI command from `rag-cli` to `rag`
- Made `lightrag-hku` and `docling` default dependencies (no extras required for basic usage)
- Updated README with `uv tool install` instructions and global usage examples

### Fixed
- Optional workspace resolution (accepts `None` for default behavior)
- HOME environment variable respected on Windows for test compatibility

### Notes
- All existing tests pass (`uv run pytest -q`)
- Backward compatible: `--workspace` override still works for project-local workflows