from langchain_core.messages import HumanMessage, SystemMessage
from app.llm.model import get_model


def main():
    model = get_model()

    messages = [
        SystemMessage(content="Eres un asistente útil"),
        HumanMessage(content="Hola, ¿cómo estás?"),
    ]

    response = model.invoke(messages)

    print(response.content)


if __name__ == "__main__":
    main()
