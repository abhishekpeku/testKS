from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.models import CodeChunk
from app.storage.json_store import JsonStore
from app.utils.text import summarize_code_file


class CodeIndexService:
    def __init__(self, store: JsonStore | None = None) -> None:
        self.store = store or JsonStore()
        self.settings = get_settings()

    def index_path(self, root_path: str) -> tuple[int, int, int]:
        root = Path(root_path).resolve()
        chunks: list[CodeChunk] = []
        indexed_files = 0
        skipped_files = 0

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part.startswith(".git") or part == ".venv" or part == "__pycache__" for part in path.parts):
                skipped_files += 1
                continue
            if path.suffix.lower() not in self.settings.code_extensions:
                skipped_files += 1
                continue

            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                skipped_files += 1
                continue

            indexed_files += 1
            chunks.append(
                CodeChunk(
                    file_path=str(path.relative_to(root)),
                    language=path.suffix.lstrip(".") or "text",
                    summary=summarize_code_file(path, content),
                    content=content,
                )
            )

        self.store.replace_code_chunks(chunks)
        return indexed_files, len(chunks), skipped_files
