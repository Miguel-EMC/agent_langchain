from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_MODEL


def get_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0,
        api_key=OPENAI_API_KEY,
    )


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
    )
