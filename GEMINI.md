# GEMINI.md - Agent LangChain Project Context

Este documento proporciona el contexto necesario para trabajar en el proyecto `agent-langchain`, una aplicación de RAG (Retrieval-Augmented Generation) que permite consultar un PDF local utilizando LangChain y Google Gemini.

## Descripción del Proyecto
El proyecto es una herramienta de CLI que carga un archivo PDF, lo divide en fragmentos, genera embeddings e indexa el contenido en una base de datos vectorial en memoria. El usuario puede realizar preguntas en lenguaje natural, y el sistema responde basándose exclusivamente en el contenido del documento.

### Tecnologías Principales
- **Lenguaje:** Python 3.12+
- **Orquestación AI:** LangChain (v0.3+)
- **Modelos de LLM & Embeddings:** Google Generative AI (Gemini 2.0 Flash y Gemini Embedding 001)
- **Gestión de Dependencias:** `uv`
- **Procesamiento de PDF:** `pypdf`
- **Configuración:** `python-dotenv`

## Arquitectura del Proyecto
La estructura del código sigue un diseño modular:

- `app/main.py`: Punto de entrada que gestiona el bucle de interacción por consola.
- `app/core/config.py`: Centraliza la configuración y validación de variables de entorno.
- `app/llm/providers.py`: Proveedores de modelos de lenguaje y embeddings.
- `app/rag/pipeline.py`: Implementa el flujo de RAG (carga, división, indexación y consulta).
- `app/rag/prompts.py`: Define las plantillas de prompts utilizadas para la generación de respuestas.

## Configuración y Ejecución

### Requisitos Previos
1. Instalar `uv` (administrador de paquetes de Python).
2. Tener una API Key de Google AI (Gemini).

### Instalación
```bash
uv sync
```

### Configuración del Entorno
Crea un archivo `.env` basado en `.env.example`:
```env
GOOGLE_API_KEY=tu_api_key_aqui
PDF_PATH="/ruta/a/tu/archivo.pdf"
```

### Ejecución
Para iniciar la demo interactiva:
```bash
uv run python -m app.main
```

## Convenciones de Desarrollo
- **Tipado:** Se utiliza tipado estático (Type Hints) en todas las funciones y clases.
- **Configuración:** Toda la configuración debe pasar por `app/core/config.py`. No uses `os.getenv` directamente en otros módulos.
- **Inyección de Dependencias:** Los modelos de LLM se obtienen a través de las funciones factory en `app/llm/providers.py`.
- **RAG Estricto:** El sistema está configurado para responder *solo* basándose en el contexto proporcionado por el PDF.

## Roadmap de Mejoras (Sugerido)
- Implementar persistencia de vectores usando `PGVector` o una base de datos vectorial externa.
- Añadir soporte para múltiples archivos PDF o directorios completos.
- Implementar una interfaz web (e.g., Streamlit o FastAPI).
