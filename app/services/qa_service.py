from __future__ import annotations

from app.models import AskResponse, Citation
from app.storage.json_store import JsonStore
from app.utils.text import score_text


class QaService:
    def __init__(self, store: JsonStore | None = None) -> None:
        self.store = store or JsonStore()

    def answer(self, question: str, top_k: int) -> AskResponse:
        sources = {source.source_id: source for source in self.store.list_sources()}
        ranked_documents = sorted(
            self.store.list_document_chunks(),
            key=lambda chunk: score_text(question, chunk.chunk_text),
            reverse=True,
        )[:top_k]
        ranked_code = sorted(
            self.store.list_code_chunks(),
            key=lambda chunk: score_text(question, f"{chunk.summary}\n{chunk.content}"),
            reverse=True,
        )[:top_k]

        doc_hits = [chunk for chunk in ranked_documents if score_text(question, chunk.chunk_text) > 0]
        code_hits = [chunk for chunk in ranked_code if score_text(question, f"{chunk.summary}\n{chunk.content}") > 0]

        doc_summary = " ".join(chunk.chunk_text[:220] for chunk in doc_hits[:3]) or (
            "No relevant ingested document chunks were found for this question."
        )
        code_summary = " ".join(chunk.summary for chunk in code_hits[:3]) or (
            "No relevant indexed code files were found for this question."
        )

        answer = (
            "This answer is grounded in the currently indexed material. "
            f"Documents suggest: {doc_summary} "
            f"Code context suggests: {code_summary}"
        )
        gaps = (
            "Document retrieval is limited to sources already discovered and ingested. "
            "Code retrieval uses simple token matching in this MVP, so semantic gaps can remain."
        )

        citations: list[Citation] = []
        for chunk in doc_hits[:3]:
            source = sources.get(chunk.source_id)
            if not source:
                continue
            citations.append(
                Citation(
                    kind="document",
                    title=source.title,
                    locator=source.url,
                    snippet=chunk.chunk_text[:220],
                )
            )
        for chunk in code_hits[:3]:
            citations.append(
                Citation(
                    kind="code",
                    title=chunk.file_path,
                    locator=chunk.file_path,
                    snippet=chunk.summary,
                )
            )

        return AskResponse(
            answer=answer,
            documents_summary=doc_summary,
            code_summary=code_summary,
            assumptions_or_gaps=gaps,
            citations=citations,
        )
