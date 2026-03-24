# Investment Modelling Research Assistant

## Purpose

This document defines a new project that:

1. Connects to Perplexity for web research
2. Collects official documents related to investment modelling
3. Ingests project code and document content
4. Answers user questions using both the codebase and the collected documents

The goal is to build a research assistant that is grounded in trustworthy sources and can explain both domain knowledge and implementation logic.

## Project Goal

Create an AI assistant that can:

- search for official investment modelling documentation
- store and organize retrieved sources
- extract and chunk useful content
- understand local code used for modelling workflows
- answer questions with citations to the underlying documents
- distinguish between documented facts and code-specific behavior

## Scope

This project is intended for:

- investment modelling reference material
- valuation methodology documentation
- regulatory or standards-based finance documents
- internal or local modelling code review
- question answering over both documents and source code

This project should avoid:

- relying on random blogs when official material is available
- answering without source grounding
- treating generated summaries as equivalent to source documents

## High-Level Workflow

### 1. Research Collection

The system sends focused prompts to Perplexity such as:

- "Find official documentation for discounted cash flow modelling"
- "Find official accounting, valuation, and investment modelling standards"
- "Find official guidance from regulators, exchanges, accounting bodies, and established financial institutions"

Perplexity should return:

- source title
- source URL
- organization name
- publication or update date when available
- extracted summary
- why the source is relevant

### 2. Source Filtering

Only keep documents from trusted sources such as:

- government regulators
- stock exchanges
- accounting standards bodies
- central banks
- official investor relations or filings portals
- well-known institutional finance publishers when official guidance is not available

Examples of trusted source categories:

- SEC
- IFRS
- FASB
- CFA Institute
- World Bank
- IMF
- central bank publications
- official listed-company filings

### 3. Document Ingestion

For each approved source:

- save metadata
- download or reference the document
- convert PDF or HTML content to clean text
- split content into chunks
- generate embeddings
- store chunks in a vector database

### 4. Code Understanding

The assistant also scans the local codebase and collects:

- file structure
- function and class summaries
- configuration and dependency details
- business logic relevant to modelling
- data flow between modules

Code should be indexed separately from documents, but linked during retrieval.

### 5. Question Answering

When a user asks a question, the system should:

- classify whether the answer needs documents, code, or both
- retrieve the most relevant chunks
- synthesize a grounded answer
- cite the sources used
- clearly separate:
  - what the documents say
  - what the code currently implements
  - any assumptions or gaps

## Recommended Architecture

## Components

- `research-service`
  - calls Perplexity API
  - collects source candidates
- `source-validator`
  - checks trust rules and official-domain allowlists
- `document-ingestion-service`
  - parses HTML/PDF/documents
  - chunks and cleans text
- `code-ingestion-service`
  - scans repository files and extracts code summaries
- `retrieval-service`
  - performs vector and metadata search
- `qa-service`
  - answers questions with citations
- `metadata-store`
  - stores source info, tags, dates, and processing state
- `vector-store`
  - stores embeddings for documents and code chunks

## Suggested Tech Stack

- Backend: FastAPI
- LLM orchestration: Python
- Search/retrieval: FAISS, Chroma, or Azure AI Search
- Parsing: `pypdf`, `beautifulsoup4`, `markdownify`, `unstructured`
- Embeddings: OpenAI or Azure OpenAI embeddings
- Storage: SQLite or PostgreSQL for metadata
- Background jobs: Celery, RQ, or FastAPI background tasks for a simple version

## Data Model

### Source Metadata

Each source should store:

- `source_id`
- `title`
- `url`
- `domain`
- `organization`
- `document_type`
- `published_date`
- `retrieved_date`
- `trust_level`
- `summary`
- `tags`
- `status`

### Document Chunk

Each chunk should store:

- `chunk_id`
- `source_id`
- `chunk_text`
- `chunk_index`
- `section_title`
- `embedding`

### Code Chunk

Each code chunk should store:

- `code_chunk_id`
- `file_path`
- `symbol_name`
- `language`
- `summary`
- `content`
- `embedding`

## Perplexity Integration Requirements

The Perplexity integration should support:

- targeted prompts for official-source discovery
- domain-aware filtering
- extraction of source URLs and summaries
- repeatable collection jobs by topic

Example research topics:

- DCF modelling
- comparable company analysis
- precedent transaction analysis
- financial statement forecasting
- cost of capital
- terminal value
- sensitivity analysis
- valuation assumptions
- capital structure
- equity research modelling practices

## Retrieval and Answering Rules

The assistant should always:

- prefer official documents over secondary summaries
- cite the exact source URL when possible
- tell the user when an answer is based on code inference rather than documentation
- mention when documents conflict or are outdated
- separate regulatory guidance from implementation choices

The assistant should not:

- invent unsupported finance rules
- hide uncertainty
- present non-official interpretations as official standards

## Example User Questions

- "What do official sources say about discount rate assumptions in DCF modelling?"
- "Which documents in our knowledge base explain terminal value best?"
- "How does our code calculate projected free cash flow?"
- "Is our implementation aligned with the collected documentation?"
- "Which part of the code handles scenario analysis?"

## MVP Plan

### Phase 1

- create a FastAPI backend
- add Perplexity research endpoint
- store discovered source metadata
- ingest a small set of approved documents
- index local code files
- build a simple ask endpoint for grounded Q&A

### Phase 2

- add PDF and HTML parsing pipeline
- add vector search
- add source trust scoring
- add answer citations and traceability
- add document refresh workflow

### Phase 3

- add UI for searching documents and asking questions
- add comparison mode for code vs documentation
- add topic-based research jobs
- add feedback loop for answer quality

## Suggested API Endpoints

- `POST /research/discover`
  - discover official sources for a modelling topic
- `POST /sources/ingest`
  - ingest selected source content
- `POST /code/index`
  - index local project code
- `POST /ask`
  - answer a question using documents and code
- `GET /sources`
  - list stored sources
- `GET /sources/{id}`
  - inspect a source and its chunks

## Output Expectations

Each answer should include:

- a direct answer
- cited source list
- relevant code references when applicable
- confidence or uncertainty note
- missing-information note if retrieval is incomplete

## Security and Compliance Notes

- store API keys in environment variables
- log source provenance
- respect robots, licenses, and document usage restrictions
- avoid storing sensitive internal code outside approved systems
- maintain clear boundaries between external documents and internal analysis

## Environment Variables

Example configuration:

```env
PERPLEXITY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
VECTOR_DB_PATH=./data/vector_store
METADATA_DB_URL=sqlite:///./data/metadata.db
TRUSTED_DOMAINS=sec.gov,ifrs.org,fasb.org,cfainstitute.org,worldbank.org,imf.org
```

## Success Criteria

This project is successful when it can:

- discover relevant official investment modelling sources
- ingest and index those sources correctly
- understand the connected codebase
- answer grounded questions with citations
- explain whether an answer comes from documents, code, or both

## Next Build Step

If we continue from this document, the next implementation step should be to create a small FastAPI service with:

- one endpoint for Perplexity source discovery
- one endpoint for local code indexing
- one endpoint for question answering over a basic in-memory or FAISS-backed index
