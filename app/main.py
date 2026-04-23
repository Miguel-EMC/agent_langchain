from app.core.config import PDF_PATH
from app.rag.pipeline import (
    ask_question,
    build_vector_store,
    load_pdf_documents,
    split_documents,
)


def main() -> None:
    print("Cargando PDF...")
    documents = load_pdf_documents(PDF_PATH)
    print(f"Paginas cargadas: {len(documents)}")

    print("Dividiendo documento en chunks...")
    chunks = split_documents(documents)
    print(f"Chunks creados: {len(chunks)}")

    print("Creando embeddings e indexando en memoria...")
    vector_store = build_vector_store(chunks)
    print("Listo. Escribe una pregunta sobre el PDF.")
    print("Escribe 'salir' para terminar.\n")

    while True:
        question = input("Pregunta: ").strip()

        if not question:
            continue

        if question.lower() in {"salir", "exit", "quit"}:
            print("Sesion finalizada.")
            break

        result = ask_question(vector_store, question)

        print("\nRespuesta:\n")
        print(result.answer)
        print("\nFuentes:")
        for source in result.sources:
            page = source["page"]
            page_label = page + 1 if isinstance(page, int) else "desconocida"
            print(f"- pagina {page_label}: {source['preview']}")
        print()


if __name__ == "__main__":
    main()
