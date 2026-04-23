from langchain_core.prompts import ChatPromptTemplate


def build_qa_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Responde usando solo el contexto recuperado del PDF. "
                    "Si la respuesta no aparece en el contexto, dilo claramente."
                ),
            ),
            (
                "human",
                (
                    "Pregunta:\n{question}\n\n"
                    "Contexto:\n{context}\n\n"
                    "Responde en espanol claro y cita paginas cuando sea posible."
                ),
            ),
        ]
    )
