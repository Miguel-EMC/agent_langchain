# Guia del Codigo

Esta guia explica el proyecto pequeno de RAG que vas a construir en vivo.

## Objetivo del proyecto

Tomar un PDF propio y permitir hacer preguntas sobre su contenido usando LangChain.

Flujo:

1. Cargar PDF
2. Dividirlo en fragmentos
3. Crear embeddings
4. Guardarlos en memoria
5. Recuperar fragmentos relevantes
6. Responder con el modelo

## Arquitectura

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

## app/core/config.py

Responsabilidad:

- Cargar variables de entorno
- Definir la ruta del PDF
- Definir modelos y parametros de chunking
- Validar configuracion minima

### Por que existe

Porque la configuracion no debe estar mezclada con la logica de negocio.

### Que contiene

- `OPENAI_API_KEY`: clave de OpenAI
- `OPENAI_MODEL`: modelo de chat
- `OPENAI_EMBEDDING_MODEL`: modelo de embeddings
- `PDF_PATH`: ruta del documento
- `CHUNK_SIZE`: tamano de cada fragmento
- `CHUNK_OVERLAP`: cuanto se solapan los fragmentos
- `RETRIEVAL_K`: cuantos fragmentos recuperar

### Idea clave para explicar

Este archivo hace que el proyecto sea portable y escalable. Si cambias de modelo o PDF, no tocas el pipeline.

## app/llm/providers.py

Responsabilidad:

- Crear el modelo conversacional
- Crear el modelo de embeddings

### Por que existe

Porque en RAG normalmente usas dos componentes distintos:

- uno para responder,
- otro para vectorizar texto.

### Funciones

#### `get_chat_model()`

Devuelve `ChatOpenAI` configurado.

Uso:

- responder preguntas
- generar la salida final

#### `get_embeddings()`

Devuelve `OpenAIEmbeddings`.

Uso:

- convertir chunks del PDF en vectores numericos
- permitir busqueda semantica

### Idea clave para explicar

El modelo de chat no reemplaza al modelo de embeddings. Cumplen funciones distintas.

## app/rag/prompts.py

Responsabilidad:

- Construir el prompt para preguntas y respuestas

### Por que existe

Porque el prompt es una pieza separada de la recuperacion y del modelo.

### Funcion

#### `build_qa_prompt()`

Construye un `ChatPromptTemplate` con:

- mensaje `system`: restringe al modelo a responder solo con el contexto recuperado
- mensaje `human`: inserta la pregunta del usuario y el contexto encontrado

### Idea clave para explicar

El prompt reduce alucinaciones porque obliga al modelo a trabajar con evidencia recuperada del PDF.

## app/rag/pipeline.py

Este es el archivo mas importante. Aqui vive el flujo completo de RAG.

### `RagAnswer`

Es una `dataclass` que devuelve:

- `answer`
- `sources`

Esto permite que tu demo sea trazable. No solo das una respuesta, tambien muestras de donde salio.

### `load_pdf_documents()`

Usa `PyPDFLoader`.

Que hace:

- lee el PDF
- devuelve una lista de `Document`
- conserva metadata como numero de pagina

Por que importa:

Luego puedes mostrar fuentes por pagina.

### `split_documents()`

Usa `RecursiveCharacterTextSplitter`.

Que hace:

- divide el PDF en chunks manejables
- evita trabajar con paginas o documentos demasiado grandes

Por que importa:

La calidad del retrieval depende mucho del chunking.

### `build_vector_store()`

Usa `InMemoryVectorStore`.

Que hace:

- genera embeddings para cada chunk
- los almacena en memoria RAM

Por que importa:

Es la forma mas simple de aprender RAG sin meter PostgreSQL ni PGVector todavia.

### `format_context()`

Que hace:

- toma los documentos recuperados
- los convierte en un texto estructurado
- agrega referencia de pagina

Por que importa:

El modelo necesita texto, no objetos Python.

### `ask_question()`

Esta es la funcion principal de consulta.

Que hace:

1. Recupera chunks similares con `similarity_search`
2. Convierte esos chunks en contexto
3. Construye la cadena LCEL
4. Ejecuta el modelo
5. Devuelve respuesta y fuentes

### La linea mas importante

```python
chain = build_qa_prompt() | get_chat_model() | StrOutputParser()
```

Esto representa la composicion moderna en LangChain:

- prompt
- modelo
- parser

## app/main.py

Responsabilidad:

- orquestar la demo en consola

### Que hace

1. Carga el PDF
2. Lo divide en chunks
3. Construye el vector store
4. Entra en un loop de preguntas
5. Imprime respuesta y fuentes

### Por que no meter logica aqui

Porque `main.py` debe ser liviano. Si luego agregas FastAPI, una interfaz web o LangGraph, no quieres reescribir el motor.

## Como conecta con tu presentacion

Tu PDF habla de:

- problema de los LLMs sin contexto
- RAG
- LangChain en tres pilares: models, prompts y retrieval
- arquitectura del sistema

Este proyecto refleja exactamente eso:

- `llm/providers.py` = models
- `rag/prompts.py` = prompts
- `rag/pipeline.py` = retrieval

## Como explicar por que no usas FastAPI en vivo

Frase recomendada:

> Para esta demo en vivo voy a construir primero el nucleo de RAG en consola, porque asi se entiende el flujo real sin distraernos con HTTP, endpoints y frontend. Despues este mismo nucleo se puede exponer con FastAPI.

## Como explicar por que no usas PGVector todavia

Frase recomendada:

> Estoy usando `InMemoryVectorStore` porque quiero enseñar primero el concepto. Cuando el flujo queda claro, cambiar a PGVector es un cambio de infraestructura, no de arquitectura mental.

## Preguntas que podrian hacerte

### Por que embeddings

Porque necesito comparar significado, no solo palabras exactas.

### Por que chunking

Porque recuperar documentos completos empeora precision, costo y contexto.

### Por que LangChain

Porque me da loaders, splitters, prompts, vector stores y composicion de cadenas en una arquitectura coherente.

### Por que no un agente

Porque aqui el problema es retrieval simple sobre un PDF. Un agente meteria complejidad sin necesidad.

## Cierre tecnico

Este proyecto es pequeno, pero ya tiene una arquitectura sana:

- configuracion separada
- modelos desacoplados
- prompt aislado
- pipeline reusable
- entrypoint simple

Eso te permite crecer luego a:

- FastAPI
- PGVector
- multiples documentos
- LangGraph
