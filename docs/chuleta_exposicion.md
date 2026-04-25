# Chuleta de Exposicion

Usa esta hoja como apoyo rapido mientras hablas. No esta hecha para leerla completa en voz alta. Esta hecha para ayudarte a no perder el hilo.

## Mensaje principal

> Un LLM no conoce mis datos privados. Con LangChain puedo conectarlo a mis documentos usando RAG.

## Objetivo de la demo

> Voy a cargar un PDF real, dividirlo en fragmentos, crear embeddings, recuperar contexto relevante y responder preguntas sobre ese documento.

## Flujo mental

`PDF -> chunks -> embeddings -> retrieval -> prompt con contexto -> respuesta`

## Orden para construir en vivo

1. `app/core/config.py`
2. `app/llm/providers.py`
3. `app/rag/prompts.py`
4. `app/rag/pipeline.py`
5. `app/main.py`

## Qué decir al abrir

> Hoy vamos a conectar un modelo de IA a nuestros propios datos usando LangChain.

> En lugar de preguntarle algo genérico a un LLM, voy a hacer que responda usando el contenido de un PDF real.

## Qué decir cuando expliques el problema

> El problema no es que el modelo sea malo. El problema es que no conoce nuestros datos privados.

> Por eso la solución no es solo un modelo más grande, sino un sistema que recupere contexto relevante.

## Qué decir cuando expliques RAG

> RAG significa Retrieval Augmented Generation.

> Primero recupero información relevante de mis datos, luego uso esa información como contexto para generar la respuesta.

## Qué decir por archivo

### `config.py`

> Aquí separo la configuración del resto de la lógica.

> Defino API key, modelo, ruta del PDF y parámetros de chunking.

### `providers.py`

> Aquí separo el modelo de chat del modelo de embeddings.

> Uno responde, el otro vectoriza texto.

### `prompts.py`

> Aquí defino el comportamiento del asistente.

> Le digo que responda solo con el contexto recuperado.

### `pipeline.py`

> Este es el núcleo de RAG.

> Aquí cargo el PDF, lo divido, creo embeddings, recupero fragmentos relevantes y ejecuto la chain.

### `main.py`

> Este archivo solo orquesta la demo.

> El motor real está en el pipeline.

## Línea más importante de todo el proyecto

```python
chain = build_qa_prompt() | get_chat_model() | StrOutputParser()
```

Qué decir:

> Esta línea representa una chain moderna en LangChain usando LCEL: prompt, modelo y parser.

## Comando para correr

```bash
uv run python -m app.main
```

## Preguntas seguras para la demo

- `¿Cuál es el problema común que resuelve este enfoque?`
- `¿Qué es RAG según la presentación?`
- `¿Cuáles son los tres pilares de LangChain?`
- `¿Por qué LangChain sigue siendo relevante en 2026?`
- `¿Qué herramientas se mencionan en la presentación?`

## Si te preguntan por FastAPI

> En las slides aparece una arquitectura más completa, pero en vivo estoy construyendo primero el núcleo de RAG para que el flujo se entienda bien. Luego esto mismo se puede exponer por FastAPI.

## Si te preguntan por PGVector

> Hoy uso `InMemoryVectorStore` para enseñar el concepto sin complejidad extra. Después este almacenamiento se puede mover a PostgreSQL con PGVector.

## Si te preguntan por qué no usas un agente

> Porque aquí el problema es retrieval simple sobre un documento. Un agente agregaría complejidad innecesaria para esta demo.

## Si te equivocas escribiendo

Di esto:

> Voy a corregir esta parte un momento.

Luego corriges y sigues. No expliques de más.

## Si te quedas en blanco

Vuelve a esta frase:

> El modelo no conoce mis datos. Entonces primero recupero contexto y luego respondo.

## Cierre

> Lo importante no es solo llamar a un LLM, sino convertirlo en un sistema que pueda trabajar con nuestros datos.

> Hoy lo hicimos con un PDF y un vector store en memoria. El siguiente paso natural sería PGVector o FastAPI.

## Recordatorio final

- habla más despacio de lo normal
- no intentes demostrar demasiado
- explica el flujo, no cada detalle a la vez
- si la demo funciona con 2 o 3 preguntas, ya salió bien
