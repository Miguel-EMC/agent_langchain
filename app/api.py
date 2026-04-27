from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.core.config import PDF_PATH
from app.rag.pipeline import (
    ask_question,
    build_vector_store,
    load_pdf_documents,
    split_documents,
)

# --- Modelos de Datos ---

from pydantic import BaseModel, Field, AliasChoices

class QuestionRequest(BaseModel):
    # Acepta "question" o "message" por si el componente de Angular usa nombres distintos
    question: str = Field(..., validation_alias=AliasChoices("question", "message", "text"))

class SourceResponse(BaseModel):
    page: int | None
    preview: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceResponse]

# --- Estado Global ---

# Almacenaremos el vector_store en una variable global para acceso rápido
# En producción, esto podría ser una DB vectorial externa
state = {"vector_store": None}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica al iniciar
    print(f"Cargando y procesando PDF: {PDF_PATH}")
    try:
        documents = load_pdf_documents(PDF_PATH)
        chunks = split_documents(documents)
        state["vector_store"] = build_vector_store(chunks)
        print("Pipeline RAG listo.")
    except Exception as e:
        print(f"Error cargando el PDF: {e}")
    yield
    # Lógica al cerrar (opcional)
    state.clear()

from fastapi.middleware.cors import CORSMiddleware

# --- Aplicación FastAPI ---

app = FastAPI(
    title="Agent RAG API",
    description="API REST para consultar documentos PDF usando LangChain y Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    if state["vector_store"] is None:
        return {"status": "error", "message": "El modelo no ha terminado de cargar el PDF"}
    return {"status": "ok", "pdf": str(PDF_PATH)}

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QuestionRequest):
    if state["vector_store"] is None:
        raise HTTPException(
            status_code=503, 
            detail="El servicio está cargando el documento, por favor intente de nuevo en unos segundos."
        )
    
    try:
        result = ask_question(state["vector_store"], request.question)
        print(f"\n--- DEBUG API ---\nPregunta: {request.question}\nRespuesta IA: {result.answer}\n-----------------\n")
        return {
            "answer": result.answer,
            "sources": [
                {"page": s["page"] + 1 if isinstance(s["page"], int) else None, "preview": s["preview"]} 
                for s in result.sources
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
