from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class SourceCandidate(BaseModel):
    title: str
    url: HttpUrl
    organization: str
    summary: str
    relevance: str
    published_date: str | None = None


class SourceRecord(BaseModel):
    source_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    url: str
    domain: str
    organization: str
    document_type: str = "web"
    published_date: str | None = None
    retrieved_date: str = Field(default_factory=utc_now)
    trust_level: Literal["official", "trusted", "unverified"] = "unverified"
    summary: str = ""
    tags: list[str] = Field(default_factory=list)
    status: Literal["discovered", "ingested", "failed"] = "discovered"


class DocumentChunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid4()))
    source_id: str
    chunk_text: str
    chunk_index: int
    section_title: str | None = None


class CodeChunk(BaseModel):
    code_chunk_id: str = Field(default_factory=lambda: str(uuid4()))
    file_path: str
    symbol_name: str | None = None
    language: str
    summary: str
    content: str


class DiscoverRequest(BaseModel):
    topic: str
    max_results: int = Field(default=5, ge=1, le=20)


class DiscoverResponse(BaseModel):
    topic: str
    used_perplexity: bool
    candidates: list[SourceRecord]
    note: str


class IngestRequest(BaseModel):
    source_id: str | None = None
    title: str | None = None
    url: str | None = None
    organization: str | None = None
    text: str | None = None
    document_type: str = "web"
    tags: list[str] = Field(default_factory=list)


class IngestResponse(BaseModel):
    source: SourceRecord
    chunks_created: int


class CodeIndexRequest(BaseModel):
    root_path: str = "."


class CodeIndexResponse(BaseModel):
    indexed_files: int
    indexed_chunks: int
    skipped_files: int


class AskRequest(BaseModel):
    question: str
    top_k: int = Field(default=5, ge=1, le=15)


class Citation(BaseModel):
    kind: Literal["document", "code"]
    title: str
    locator: str
    snippet: str


class AskResponse(BaseModel):
    answer: str
    documents_summary: str
    code_summary: str
    assumptions_or_gaps: str
    citations: list[Citation]


class SourceDetail(BaseModel):
    source: SourceRecord
    chunks: list[DocumentChunk]
