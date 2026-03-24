from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from app.config import get_settings
from app.models import CodeChunk, DocumentChunk, SourceRecord


T = TypeVar("T", bound=BaseModel)


class JsonStore:
    def __init__(self) -> None:
        data_dir = get_settings().data_dir
        self.sources_path = data_dir / "sources.json"
        self.document_chunks_path = data_dir / "document_chunks.json"
        self.code_chunks_path = data_dir / "code_chunks.json"
        self._ensure_files()

    def _ensure_files(self) -> None:
        for path in (self.sources_path, self.document_chunks_path, self.code_chunks_path):
            if not path.exists():
                path.write_text("[]", encoding="utf-8")

    def _load(self, path: Path, model_type: type[T]) -> list[T]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [model_type.model_validate(item) for item in raw]

    def _save(self, path: Path, records: list[BaseModel]) -> None:
        path.write_text(
            json.dumps([record.model_dump(mode="json") for record in records], indent=2),
            encoding="utf-8",
        )

    def list_sources(self) -> list[SourceRecord]:
        return self._load(self.sources_path, SourceRecord)

    def get_source(self, source_id: str) -> SourceRecord | None:
        return next((source for source in self.list_sources() if source.source_id == source_id), None)

    def upsert_source(self, source: SourceRecord) -> SourceRecord:
        sources = self.list_sources()
        updated = False
        for index, existing in enumerate(sources):
            if existing.source_id == source.source_id:
                sources[index] = source
                updated = True
                break
        if not updated:
            sources.append(source)
        self._save(self.sources_path, sources)
        return source

    def list_document_chunks(self) -> list[DocumentChunk]:
        return self._load(self.document_chunks_path, DocumentChunk)

    def replace_document_chunks_for_source(self, source_id: str, chunks: list[DocumentChunk]) -> None:
        existing = [chunk for chunk in self.list_document_chunks() if chunk.source_id != source_id]
        existing.extend(chunks)
        self._save(self.document_chunks_path, existing)

    def get_document_chunks(self, source_id: str) -> list[DocumentChunk]:
        return [chunk for chunk in self.list_document_chunks() if chunk.source_id == source_id]

    def list_code_chunks(self) -> list[CodeChunk]:
        return self._load(self.code_chunks_path, CodeChunk)

    def replace_code_chunks(self, chunks: list[CodeChunk]) -> None:
        self._save(self.code_chunks_path, chunks)
