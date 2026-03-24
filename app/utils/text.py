from __future__ import annotations

import re
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9_]+")


def extract_domain(url: str) -> str:
    cleaned = url.replace("https://", "").replace("http://", "")
    return cleaned.split("/")[0].lower()


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        chunks.append(normalized[start:end].strip())
        if end == len(normalized):
            break
        start = max(0, end - overlap)
    return chunks


def summarize_code_file(path: Path, content: str) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    preview = " ".join(lines[:3])[:180]
    return f"{path.name} contains {len(content.splitlines())} lines. Preview: {preview}"


def tokenize(text: str) -> set[str]:
    return {match.group(0).lower() for match in WORD_RE.finditer(text)}


def score_text(query: str, text: str) -> int:
    query_tokens = tokenize(query)
    text_tokens = tokenize(text)
    return len(query_tokens & text_tokens)
