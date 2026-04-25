import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_PDF_PATH = "/home/migueldev/Downloads/LangChain Presentation.pdf"


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
PDF_PATH = os.getenv("PDF_PATH", DEFAULT_PDF_PATH)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))


if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY. Define it in the environment or in .env.")

if not Path(PDF_PATH).exists():
    raise RuntimeError(f"PDF not found at: {PDF_PATH}")
