# Investment Modelling Research Assistant

A FastAPI project that can discover official investment-modelling sources, ingest document text, index local code, and answer grounded questions using both document and code context.

## Features

- Perplexity-backed source discovery when `PERPLEXITY_API_KEY` is configured
- Curated fallback sources when the API key is not configured
- Trusted-domain classification for official-source prioritization
- Document ingestion and chunking
- Local code indexing for repository understanding
- Question answering with document and code citations
- JSON-backed persistence in `data/`

## Project Structure

```text
app/
  main.py
  config.py
  models.py
  services/
  storage/
  utils/
data/
run.py
requirements.txt
.env.example
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your API keys to `.env` if you want live Perplexity discovery.

## Run

```powershell
python run.py
```

Open:

- `http://localhost:8000`
- `http://localhost:8000/docs`

## Example API Flow

### 1. Discover official sources

```powershell
curl -X POST http://localhost:8000/research/discover -H "Content-Type: application/json" -d '{"topic":"discounted cash flow modelling","max_results":5}'
```

### 2. Ingest a document using pasted text

```powershell
curl -X POST http://localhost:8000/sources/ingest -H "Content-Type: application/json" -d '{"title":"DCF Notes","url":"https://example.com/dcf","organization":"Example Org","text":"Discounted cash flow models estimate enterprise value by forecasting free cash flow and discounting it.","tags":["dcf"]}'
```

### 3. Index the local codebase

```powershell
curl -X POST http://localhost:8000/code/index -H "Content-Type: application/json" -d '{"root_path":"."}'
```

### 4. Ask a grounded question

```powershell
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question":"How does this project combine official documents and code understanding?","top_k":5}'
```

## Notes

- Live web retrieval depends on network access and a valid Perplexity API key.
- This MVP uses simple token-overlap retrieval rather than embeddings.
- `data/` stores discovered sources, document chunks, and code chunks as JSON.
