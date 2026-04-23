from langchain_openai import ChatOpenAI
from app.config import OPENAI_API_KEY


def get_model():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.9,
        api_key=OPENAI_API_KEY,
    )
