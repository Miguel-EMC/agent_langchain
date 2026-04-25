# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the app
uv run python -m app.main

# Run a single test (no test suite yet)
uv run pytest tests/path/to/test_file.py::test_name
```

## Architecture

PDF RAG pipeline with Google Generative AI, console Q&A loop.

**Data flow:** PDF file → `PyPDFLoader` (page mode) → `RecursiveCharacterTextSplitter` → `InMemoryVectorStore` (Google embeddings) → similarity search → `ChatPromptTemplate` | `ChatGoogleGenerativeAI` | `StrOutputParser` → `RagAnswer`

**Module responsibilities:**
- `app/core/config.py` — loads `.env`, exposes all config constants. Raises `RuntimeError` at import time if `GOOGLE_API_KEY` missing or PDF path doesn't exist. Validates eagerly so failures surface before any LLM call.
- `app/llm/providers.py` — factory functions `get_chat_model()` / `get_embeddings()` returning Google GenAI instances. Swap provider here only.
- `app/rag/prompts.py` — `build_qa_prompt()` returns the single `ChatPromptTemplate` used by the chain.
- `app/rag/pipeline.py` — four pure pipeline steps (`load_pdf_documents`, `split_documents`, `build_vector_store`, `ask_question`) plus `RagAnswer` dataclass. `ask_question` rebuilds the chain on every call (stateless).
- `app/main.py` — REPL loop, builds vector store once at startup, calls `ask_question` per iteration.

## Configuration

`.env.example` is stale — it shows `OPENAI_*` keys but the codebase uses Google GenAI. Actual required keys:

```
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-2.0-flash          # default fallback is "gpt-5-mini" (wrong — set explicitly)
GOOGLE_EMBEDDING_MODEL=models/text-embedding-004
PDF_PATH=/path/to/your.pdf
CHUNK_SIZE=1200
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

## Key design notes

- Vector store is in-memory only — rebuilt on every run, no persistence.
- Next upgrade: replace `InMemoryVectorStore` with `PGVector` (PostgreSQL) for persistence.
- The chain in `ask_question` calls `get_chat_model()` on every question — fine for demo, inefficient at scale.
- Prompts are Spanish-language by default (`prompts.py` instructs the model to answer in Spanish).
