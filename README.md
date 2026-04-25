# LangChain PDF RAG

Proyecto pequeno para exponer:

1. cargar un PDF propio,
2. convertirlo en chunks,
3. generar embeddings,
4. recuperar fragmentos relevantes,
5. responder preguntas con LangChain.

## Estructura

```text
app/
├── core/
│   └── config.py
├── llm/
│   └── providers.py
├── rag/
│   ├── pipeline.py
│   └── prompts.py
└── main.py
```

## Configuracion

1. Crea `.env` a partir de `.env.example`
2. Coloca tu API key de OpenAI
3. Ajusta la ruta del PDF si hace falta

## Ejecutar

```bash
uv sync
uv run python -m app.main
```

## Flujo de la demo

- El programa carga el PDF una sola vez al iniciar.
- Divide el contenido en fragmentos.
- Crea embeddings.
- Guarda esos embeddings en memoria.
- Permite hacer preguntas en consola.

## Siguiente paso despues de esta demo

Cuando entiendas esta version, el siguiente upgrade natural es cambiar el vector store en memoria por `PGVector` sobre PostgreSQL.
