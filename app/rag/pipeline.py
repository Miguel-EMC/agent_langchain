from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import CHUNK_OVERLAP, CHUNK_SIZE, PDF_PATH, RETRIEVAL_K
from app.llm.providers import get_chat_model, get_embeddings
from app.rag.prompts import build_qa_prompt


@dataclass
class RagAnswer:
    answer: str
    sources: list[dict]


def load_pdf_documents(pdf_path: str | Path = PDF_PATH) -> list[Document]:
    loader = PyPDFLoader(str(pdf_path), mode="page")
    return loader.load()


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks: list[Document]) -> InMemoryVectorStore:
    vector_store = InMemoryVectorStore(get_embeddings())
    vector_store.add_documents(chunks)
    return vector_store


def format_context(documents: list[Document]) -> str:
    parts: list[str] = []
    for index, document in enumerate(documents, start=1):
        page = document.metadata.get("page")
        page_label = page + 1 if isinstance(page, int) else "desconocida"
        parts.append(f"[Fragmento {index} | pagina {page_label}]\n{document.page_content}")
    return "\n\n".join(parts)


def ask_question(vector_store: InMemoryVectorStore, question: str) -> RagAnswer:
    retrieved_docs = vector_store.similarity_search(question, k=RETRIEVAL_K)
    context = format_context(retrieved_docs)

    chain = build_qa_prompt() | get_chat_model() | StrOutputParser()
    answer = chain.invoke({"question": question, "context": context})

    sources = [
        {
            "page": document.metadata.get("page", None),
            "preview": document.page_content[:180].replace("\n", " "),
        }
        for document in retrieved_docs
    ]

    return RagAnswer(answer=answer, sources=sources)
