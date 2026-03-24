from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from app.models import DocumentChunk, IngestRequest, SourceRecord
from app.services.source_validator import SourceValidator
from app.storage.json_store import JsonStore
from app.utils.text import chunk_text, extract_domain


class IngestionService:
    def __init__(self, store: JsonStore | None = None) -> None:
        self.store = store or JsonStore()
        self.validator = SourceValidator()

    def ingest(self, request: IngestRequest) -> tuple[SourceRecord, int]:
        source = self._resolve_source(request)
        text = request.text or self._fetch_text(source.url)
        chunks = [
            DocumentChunk(source_id=source.source_id, chunk_text=chunk, chunk_index=index)
            for index, chunk in enumerate(chunk_text(text))
        ]
        source.status = "ingested"
        self.store.upsert_source(source)
        self.store.replace_document_chunks_for_source(source.source_id, chunks)
        return source, len(chunks)

    def _resolve_source(self, request: IngestRequest) -> SourceRecord:
        if request.source_id:
            source = self.store.get_source(request.source_id)
            if not source:
                raise ValueError(f"Source '{request.source_id}' was not found.")
            if request.tags:
                source.tags = sorted(set(source.tags + request.tags))
            return source

        if not request.title or not request.url or not request.organization:
            raise ValueError("title, url, and organization are required when source_id is not provided.")

        domain = extract_domain(request.url)
        source = SourceRecord(
            title=request.title,
            url=request.url,
            domain=domain,
            organization=request.organization,
            document_type=request.document_type,
            trust_level=self.validator.classify(domain),
            tags=request.tags,
        )
        return self.store.upsert_source(source)

    def _fetch_text(self, url: str) -> str:
        response = requests.get(url, timeout=45)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").lower()
        if "html" in content_type:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(" ", strip=True)
        return response.text
