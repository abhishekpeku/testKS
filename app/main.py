from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.models import (
    AskRequest,
    AskResponse,
    CodeIndexRequest,
    CodeIndexResponse,
    DiscoverRequest,
    DiscoverResponse,
    IngestRequest,
    IngestResponse,
    SourceDetail,
    SourceRecord,
)
from app.services.code_index_service import CodeIndexService
from app.services.ingestion_service import IngestionService
from app.services.qa_service import QaService
from app.services.research_service import ResearchService
from app.storage.json_store import JsonStore


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
store = JsonStore()
research_service = ResearchService()
ingestion_service = IngestionService(store)
code_index_service = CodeIndexService(store)
qa_service = QaService(store)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": settings.app_name}


@app.post("/research/discover", response_model=DiscoverResponse)
def discover_sources(request: DiscoverRequest) -> DiscoverResponse:
    candidates, used_perplexity, note = research_service.discover(request)
    saved: list[SourceRecord] = []
    for candidate in candidates:
        saved.append(store.upsert_source(candidate))
    return DiscoverResponse(
        topic=request.topic,
        used_perplexity=used_perplexity,
        candidates=saved,
        note=note,
    )


@app.post("/sources/ingest", response_model=IngestResponse)
def ingest_source(request: IngestRequest) -> IngestResponse:
    try:
        source, count = ingestion_service.ingest(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}") from exc
    return IngestResponse(source=source, chunks_created=count)


@app.post("/code/index", response_model=CodeIndexResponse)
def index_code(request: CodeIndexRequest) -> CodeIndexResponse:
    indexed_files, indexed_chunks, skipped_files = code_index_service.index_path(request.root_path)
    return CodeIndexResponse(
        indexed_files=indexed_files,
        indexed_chunks=indexed_chunks,
        skipped_files=skipped_files,
    )


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> AskResponse:
    return qa_service.answer(request.question, request.top_k)


@app.get("/sources", response_model=list[SourceRecord])
def list_sources() -> list[SourceRecord]:
    return store.list_sources()


@app.get("/sources/{source_id}", response_model=SourceDetail)
def get_source(source_id: str) -> SourceDetail:
    source = store.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found.")
    return SourceDetail(source=source, chunks=store.get_document_chunks(source_id))
