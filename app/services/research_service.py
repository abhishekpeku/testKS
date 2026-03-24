from __future__ import annotations

import json

import requests

from app.config import get_settings
from app.models import DiscoverRequest, SourceCandidate, SourceRecord
from app.services.source_validator import SourceValidator
from app.utils.text import extract_domain


class ResearchService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.validator = SourceValidator()

    def discover(self, request: DiscoverRequest) -> tuple[list[SourceRecord], bool, str]:
        if not self.settings.perplexity_api_key:
            candidates = self._fallback_candidates(request.topic, request.max_results)
            return candidates, False, "Perplexity API key not configured, returned curated starter sources."

        prompt = self._build_prompt(request.topic, request.max_results)
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {self.settings.perplexity_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.settings.perplexity_model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Return only JSON. Find official or primary-source documents for investment "
                            "modelling. Include title, url, organization, summary, relevance, and "
                            "published_date when available."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.1,
            },
            timeout=45,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        payload = json.loads(content)
        records: list[SourceRecord] = []
        for item in payload[: request.max_results]:
            candidate = SourceCandidate.model_validate(item)
            domain = extract_domain(str(candidate.url))
            records.append(
                SourceRecord(
                    title=candidate.title,
                    url=str(candidate.url),
                    domain=domain,
                    organization=candidate.organization,
                    published_date=candidate.published_date,
                    trust_level=self.validator.classify(domain),
                    summary=candidate.summary,
                    tags=[request.topic],
                )
            )
        return records, True, "Results returned from Perplexity."

    def _build_prompt(self, topic: str, max_results: int) -> str:
        return (
            f"Topic: {topic}. Find up to {max_results} official documents or primary sources related to "
            "investment modelling, valuation, accounting standards, regulators, or institutional finance "
            "guidance. Prefer official domains and avoid blogs. Return a JSON array."
        )

    def _fallback_candidates(self, topic: str, max_results: int) -> list[SourceRecord]:
        starter = [
            {
                "title": "SEC Filings and Forms",
                "url": "https://www.sec.gov/forms",
                "organization": "U.S. Securities and Exchange Commission",
                "summary": "Primary-source regulatory filings and disclosure documents useful for valuation inputs.",
            },
            {
                "title": "IFRS Accounting Standards",
                "url": "https://www.ifrs.org/issued-standards/list-of-standards/",
                "organization": "IFRS Foundation",
                "summary": "Official accounting standards that influence financial modelling assumptions and treatment.",
            },
            {
                "title": "FASB Accounting Standards Codification Overview",
                "url": "https://www.fasb.org/page/PageContent?pageId=/standards/accounting-standards-codification.html",
                "organization": "Financial Accounting Standards Board",
                "summary": "Official U.S. GAAP standards reference relevant to model input treatment and disclosures.",
            },
            {
                "title": "CFA Institute Research and Policy Center",
                "url": "https://rpc.cfainstitute.org/",
                "organization": "CFA Institute",
                "summary": "Professional finance and valuation guidance from a well-established institutional body.",
            },
            {
                "title": "World Bank Open Knowledge Repository",
                "url": "https://openknowledge.worldbank.org/",
                "organization": "World Bank",
                "summary": "Institutional research and finance references for macroeconomic and valuation context.",
            },
        ]
        records: list[SourceRecord] = []
        for item in starter[:max_results]:
            domain = extract_domain(item["url"])
            records.append(
                SourceRecord(
                    title=item["title"],
                    url=item["url"],
                    domain=domain,
                    organization=item["organization"],
                    trust_level=self.validator.classify(domain),
                    summary=f"{item['summary']} Topic seed: {topic}.",
                    tags=[topic],
                )
            )
        return records
