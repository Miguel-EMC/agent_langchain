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

### Codigo actual

```python
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
```

### Explicacion linea por linea

#### `from langchain_core.prompts import ChatPromptTemplate`

Importa `ChatPromptTemplate`, la clase de LangChain para construir prompts conversacionales.

Por que se usa:

- trabajamos con un chat model
- queremos separar mensajes `system` y `human`
- es mas limpio que concatenar strings manualmente

#### Linea en blanco

Separa imports de funciones.

#### `def build_qa_prompt() -> ChatPromptTemplate:`

Define una funcion que construye y devuelve un prompt.

Partes:

- `def`: define una funcion
- `build_qa_prompt`: nombre claro de la funcion
- `()`: no recibe parametros porque el template es fijo
- `-> ChatPromptTemplate`: indica el tipo de retorno

Por que usar una funcion:

- evita dejar el prompt como variable global suelta
- permite reutilizarlo
- deja abierto modificarlo luego

#### `return ChatPromptTemplate.from_messages(`

Devuelve directamente un prompt creado a partir de mensajes.

Por que `from_messages`:

- porque este prompt tiene estructura de conversacion
- cada mensaje tiene rol y contenido

#### `[`

Aqui los corchetes crean una lista real.

Por que una lista:

- porque el prompt tiene varios mensajes
- el orden importa

#### `(`

Empieza una tupla.

Por que una tupla:

- cada mensaje se define como `(rol, contenido)`
- es una forma compacta y clara

#### `"system",`

Es el rol del primer mensaje.

Por que `system`:

- define las reglas generales del asistente
- controla comportamiento global

#### `(`

Abre un grupo de strings entre parentesis.

Por que:

- en Python puedes juntar varios strings entre parentesis
- mejora legibilidad si el texto es largo

#### `"Responde usando solo el contexto recuperado del PDF. "`

Primera parte del mensaje de sistema.

Por que termina en espacio:

- porque se concatena automaticamente con el siguiente string
- ese espacio evita pegar palabras

#### `"Si la respuesta no aparece en el contexto, dilo claramente."`

Segunda parte del mensaje de sistema.

Por que se divide en dos strings:

- para que no quede una linea demasiado larga
- es mas facil de leer y editar

#### `),`

Cierra el bloque de texto del mensaje `system`.

#### `),`

Cierra la tupla completa del primer mensaje.

#### `(`

Empieza la tupla del segundo mensaje.

#### `"human",`

Es el rol del segundo mensaje.

Por que `human`:

- representa la entrada del usuario
- aqui van la pregunta y el contexto dinamico

#### `(`

Abre el texto del mensaje humano.

#### `"Pregunta:\n{question}\n\n"`

Primera parte del mensaje humano.

Partes:

- `"Pregunta:"`: etiqueta visual
- `\n`: salto de linea
- `{question}`: variable del prompt
- `\n\n`: deja una linea en blanco

Por que `{question}`:

- es un placeholder
- en tiempo de ejecucion sera reemplazado por la pregunta real

#### `"Contexto:\n{context}\n\n"`

Segunda parte del mensaje humano.

Por que `{context}`:

- aqui se inserta el texto recuperado del vector store
- es la base factual de la respuesta

#### `"Responde en espanol claro y cita paginas cuando sea posible."`

Ultima parte del mensaje humano.

Por que existe:

- fuerza estilo de salida
- intenta que la respuesta sea util para demo

#### `)`

Cierra el texto del mensaje humano.

#### `),`

Cierra la tupla del mensaje humano.

#### `]`

Cierra la lista de mensajes.

#### `)`

Cierra la llamada a `from_messages`.

### Resumen conceptual de `prompts.py`

Este archivo define las reglas de respuesta del sistema.

Su trabajo no es buscar informacion ni llamar al modelo. Su trabajo es decirle al modelo:

- como debe comportarse
- que datos va a recibir
- como debe responder

### Speech tecnico corto para `prompts.py`

> Este archivo encapsula el prompt del sistema. Uso `ChatPromptTemplate` porque estoy trabajando con un chat model y necesito separar claramente el mensaje de sistema del mensaje del usuario. El mensaje de sistema restringe la respuesta al contexto recuperado del PDF, y el mensaje humano inserta dos variables dinamicas: la pregunta y el contexto encontrado. Asi reduzco alucinaciones y mantengo el prompt desacoplado del pipeline.

## app/rag/pipeline.py

Este es el archivo mas importante. Aqui vive el flujo completo de RAG.

Codigo actual:

```python
from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import CHUNK_OVERLAP, CHUNK_SIZE, PDF_PATH, RETRIEVAL_K
from app.llm.providers import get_chat_model, get_embeddings
from app.rag.prompts import build_qa_prompt


@dataclass
class RagAnswer:
    answer: str
    sources: list[dict]


def load_pdf_documents(pdf_path: str | Path = PDF_PATH) -> list[Document]:
    loader = PyPDFLoader(str(pdf_path), mode="page")
    return loader.load()


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks: list[Document]) -> InMemoryVectorStore:
    vector_store = InMemoryVectorStore(get_embeddings())
    vector_store.add_documents(chunks)
    return vector_store


def format_context(documents: list[Document]) -> str:
    parts: list[str] = []
    for index, document in enumerate(documents, start=1):
        page = document.metadata.get("page")
        page_label = page + 1 if isinstance(page, int) else "desconocida"
        parts.append(f"[Fragmento {index} | pagina {page_label}]\n{document.page_content}")
    return "\n\n".join(parts)


def ask_question(vector_store: InMemoryVectorStore, question: str) -> RagAnswer:
    retrieved_docs = vector_store.similarity_search(question, k=RETRIEVAL_K)
    context = format_context(retrieved_docs)

    chain = build_qa_prompt() | get_chat_model() | StrOutputParser()
    answer = chain.invoke({"question": question, "context": context})

    sources = [
        {
            "page": document.metadata.get("page", None),
            "preview": document.page_content[:180].replace("\n", " "),
        }
        for document in retrieved_docs
    ]

    return RagAnswer(answer=answer, sources=sources)
```

### Explicacion linea por linea

#### `from dataclasses import dataclass`

Importa `dataclass`, una utilidad de Python para crear clases de datos simples sin escribir manualmente el constructor.

Por que se usa aqui:

- porque `RagAnswer` solo guarda datos
- no necesita logica compleja
- evita escribir `__init__`, `__repr__` y otras cosas repetitivas

#### `from pathlib import Path`

Importa `Path`, una forma moderna de trabajar con rutas de archivos.

Por que se usa:

- hace el codigo mas claro que usar strings sueltos
- representa rutas de forma tipada
- funciona mejor para operaciones de archivos

#### `from langchain_community.document_loaders import PyPDFLoader`

Importa el loader que sabe abrir y leer PDFs.

Por que se usa:

- queremos convertir un PDF en objetos `Document`
- LangChain ya trae esta abstraccion lista

#### `from langchain_core.documents import Document`

Importa el tipo `Document`.

Por que se usa:

- para indicar claramente que nuestras funciones trabajan con documentos LangChain
- para mejorar legibilidad y tipado

#### `from langchain_core.output_parsers import StrOutputParser`

Importa un parser que convierte la salida del modelo en texto plano.

Por que se usa:

- el modelo devuelve un objeto de mensaje
- nosotros queremos un `str` simple para imprimirlo en consola

#### `from langchain_core.vectorstores import InMemoryVectorStore`

Importa un vector store en memoria.

Por que se usa:

- permite guardar embeddings sin base de datos
- es perfecto para una demo inicial

#### `from langchain_text_splitters import RecursiveCharacterTextSplitter`

Importa el splitter de texto.

Por que se usa:

- divide documentos grandes en fragmentos mas pequenos
- ayuda a que la recuperacion sea mas precisa

#### `from app.core.config import CHUNK_OVERLAP, CHUNK_SIZE, PDF_PATH, RETRIEVAL_K`

Importa configuraciones desde otro modulo.

Por que se usa:

- evita hardcodear valores aqui
- separa configuracion de logica

#### `from app.llm.providers import get_chat_model, get_embeddings`

Importa funciones que crean el modelo de chat y el de embeddings.

Por que se usa:

- este archivo no debe conocer detalles internos de OpenAI
- solo necesita pedir un modelo y unas embeddings

#### `from app.rag.prompts import build_qa_prompt`

Importa la funcion que construye el prompt.

Por que se usa:

- mantiene el prompt separado del pipeline
- deja claro que prompt y retrieval son piezas distintas

#### Linea en blanco

Las lineas en blanco no son decoracion. Sirven para separar bloques logicos y hacer el codigo mas legible.

#### `@dataclass`

Es un decorador.

Que significa:

- el simbolo `@` en Python aplica una transformacion a la clase o funcion que viene justo debajo
- aqui le dice a Python que `RagAnswer` es una dataclass

#### `class RagAnswer:`

Define una clase llamada `RagAnswer`.

Por que existe:

- para devolver una respuesta estructurada
- para no devolver una tupla poco clara como `(answer, sources)`

#### `answer: str`

Declara un atributo llamado `answer` de tipo `str`.

Por que se usa:

- `answer` guardara la respuesta final del modelo
- `: str` es una anotacion de tipo, no una conversion

#### `sources: list[dict]`

Declara un atributo llamado `sources`.

Por que `list[dict]`:

- `list[...]` significa una lista
- los corchetes `[]` aqui no crean una lista real; en este caso forman parte de la anotacion de tipo
- `dict` indica que cada elemento de la lista sera un diccionario

En otras palabras:

- `sources` sera una lista
- cada item de esa lista tendra estructura tipo diccionario

Ejemplo mental:

```python
[
    {"page": 2, "preview": "texto..."},
    {"page": 5, "preview": "otro texto..."}
]
```

#### Linea en blanco

Separa la definicion de la clase de la primera funcion.

#### `def load_pdf_documents(pdf_path: str | Path = PDF_PATH) -> list[Document]:`

Define una funcion.

Partes:

- `def`: palabra clave para crear funciones
- `load_pdf_documents`: nombre de la funcion
- `pdf_path`: parametro de entrada
- `: str | Path`: el parametro puede ser string o `Path`
- `= PDF_PATH`: si no pasas nada, usa la ruta por defecto
- `-> list[Document]`: indica que la funcion devuelve una lista de objetos `Document`

Por que `str | Path`:

- permite flexibilidad
- puedes pasar una ruta como texto o como objeto `Path`

Por que `list[Document]`:

- los corchetes `[]` en este caso significan "lista de"
- no es indexacion ni creacion de lista

#### `loader = PyPDFLoader(str(pdf_path), mode="page")`

Crea una variable llamada `loader`.

Por que `loader`:

- es el objeto responsable de leer el PDF

Por que `str(pdf_path)`:

- aunque `pdf_path` puede ser `Path`, el loader espera una cadena de texto
- `str(...)` convierte la ruta a string

Por que `mode="page"`:

- indica que el PDF debe cargarse por pagina
- eso hace que cada pagina se convierta en un `Document`
- asi despues puedes citar paginas

#### `return loader.load()`

Ejecuta la carga del PDF y devuelve el resultado.

Por que se devuelve directo:

- no hace falta guardar el resultado en una variable intermedia si solo se va a retornar

#### Linea en blanco

Separa funciones.

#### `def split_documents(documents: list[Document]) -> list[Document]:`

Define una funcion para dividir documentos.

Por que `documents`:

- es el nombre del parametro porque la funcion recibe varios documentos

Por que `list[Document]`:

- el argumento es una lista de documentos
- el resultado tambien es una lista de documentos

Diferencia:

- entrada: documentos mas grandes
- salida: documentos fragmentados

#### `splitter = RecursiveCharacterTextSplitter(`

Crea una variable llamada `splitter`.

Por que existe:

- encapsula la estrategia de dividir texto

#### `chunk_size=CHUNK_SIZE,`

Define el tamano maximo aproximado de cada chunk.

Por que se usa una variable:

- para poder cambiarlo desde configuracion
- para experimentar sin tocar la logica

#### `chunk_overlap=CHUNK_OVERLAP,`

Define cuanto texto se repite entre un chunk y el siguiente.

Por que sirve:

- evita perder contexto en los bordes
- si una idea empieza al final de un chunk, el overlap ayuda a que no se corte mal

#### `)`

Cierra la construccion del splitter.

#### `return splitter.split_documents(documents)`

Aplica el splitter a la lista de documentos.

Por que se llama `split_documents`:

- porque el input es una lista de `Document`
- no una cadena de texto cruda

#### Linea en blanco

Separa funciones.

#### `def build_vector_store(chunks: list[Document]) -> InMemoryVectorStore:`

Define una funcion para construir el almacen vectorial.

Por que el parametro se llama `chunks`:

- porque ya no son paginas completas
- ahora son fragmentos listos para vectorizar

#### `vector_store = InMemoryVectorStore(get_embeddings())`

Crea un vector store y le pasa el modelo de embeddings.

Por que `get_embeddings()` va dentro:

- el vector store necesita saber como convertir texto en vectores

Por que se llama `vector_store`:

- describe claramente que guarda vectores

#### `vector_store.add_documents(chunks)`

Agrega los chunks al vector store.

Que pasa internamente:

- toma cada chunk
- calcula su embedding
- lo guarda junto con el contenido y metadata

#### `return vector_store`

Devuelve el vector store ya listo para consultas.

#### Linea en blanco

Separa funciones.

#### `def format_context(documents: list[Document]) -> str:`

Define una funcion para convertir documentos recuperados en un string de contexto.

Por que devuelve `str`:

- porque el modelo necesita texto dentro del prompt
- no puede recibir una lista arbitraria de objetos Python

#### `parts: list[str] = []`

Esta linea es importante.

Partes:

- `parts`: nombre de la variable
- `: list[str]`: indica que sera una lista de strings
- `= []`: crea una lista vacia

Por que `[]` aqui:

- aqui los corchetes si crean una lista real vacia
- luego iremos agregando textos a esa lista

Por que no concatenar strings directamente:

- acumular fragmentos en lista y luego hacer `join` es mas limpio
- evita concatenaciones repetidas

#### `for index, document in enumerate(documents, start=1):`

Empieza un bucle.

Partes:

- `for`: recorre elementos
- `index, document`: en cada vuelta obtienes posicion y documento
- `enumerate(...)`: agrega contador automatico
- `start=1`: el contador empieza en 1, no en 0

Por que se usa:

- para etiquetar cada fragmento como Fragmento 1, Fragmento 2, etc.

#### `page = document.metadata.get("page")`

Busca la pagina en la metadata del documento.

Por que `.get("page")`:

- evita error si la clave no existe
- si no existe, devuelve `None`

#### `page_label = page + 1 if isinstance(page, int) else "desconocida"`

Usa una expresion condicional.

Que hace:

- si `page` es entero, suma 1
- si no, pone `"desconocida"`

Por que suma 1:

- muchas librerias indexan desde 0
- para personas es mas natural mostrar pagina 1, 2, 3

#### `parts.append(f"[Fragmento {index} | pagina {page_label}]\\n{document.page_content}")`

Agrega un string a la lista `parts`.

Partes:

- `parts.append(...)`: agrega un elemento al final de la lista
- `f"..."`: f-string, permite insertar variables dentro del string
- `{index}` y `{page_label}`: se reemplazan con valores reales
- `\n`: salto de linea
- `document.page_content`: contenido textual del documento

Por que usar `append`:

- porque queremos guardar un bloque de texto por cada documento recuperado

#### `return "\\n\\n".join(parts)`

Une todos los strings de `parts` en un solo string.

Por que `"\n\n"`:

- deja una linea en blanco entre fragmentos
- hace el contexto mas legible

Por que `join(parts)`:

- convierte una lista de strings en un string unico

#### Linea en blanco

Separa funciones.

#### `def ask_question(vector_store: InMemoryVectorStore, question: str) -> RagAnswer:`

Define la funcion principal de consulta.

Parametros:

- `vector_store`: el almacen con embeddings
- `question`: la pregunta del usuario

Devuelve:

- un `RagAnswer`

#### `retrieved_docs = vector_store.similarity_search(question, k=RETRIEVAL_K)`

Hace busqueda semantica.

Por que se usa:

- convierte la pregunta en embedding
- compara contra los embeddings guardados
- devuelve los `k` chunks mas parecidos

Por que `k=RETRIEVAL_K`:

- limita cuantas fuentes traer
- ayuda a controlar contexto y costo

#### `context = format_context(retrieved_docs)`

Convierte los documentos recuperados en un string de contexto.

Por que guardar en variable:

- porque ese contexto se usara inmediatamente en la chain
- mejora legibilidad

#### `chain = build_qa_prompt() | get_chat_model() | StrOutputParser()`

Esta es la cadena LCEL.

Partes:

- `build_qa_prompt()`: genera el prompt
- `|`: pasa la salida del paso anterior al siguiente
- `get_chat_model()`: ejecuta el modelo
- `StrOutputParser()`: transforma la salida a string

Por que el simbolo `|`:

- en LCEL significa composicion de pasos
- se lee como un pipeline

#### `answer = chain.invoke({"question": question, "context": context})`

Ejecuta la chain.

Por que se pasa un diccionario:

- el prompt espera variables con nombre
- esas variables son `question` y `context`

Por que `{}` aqui:

- las llaves crean un diccionario en Python
- `"question": question` significa clave `question`, valor contenido en la variable `question`
- `"context": context` significa clave `context`, valor contenido en la variable `context`

#### `sources = [`

Empieza una list comprehension.

Por que `[]` aqui:

- en este caso los corchetes crean una lista
- esa lista se llenara con un diccionario por cada documento recuperado

#### `{`

Abre un diccionario.

Por que se usa un diccionario:

- queremos devolver varias piezas por fuente
- pagina
- preview

#### `"page": document.metadata.get("page", None),`

Guarda la pagina de origen.

Por que `.get("page", None)`:

- si la metadata no tiene `page`, el valor sera `None`
- evita errores

#### `"preview": document.page_content[:180].replace("\\n", " "),`

Construye un resumen corto del chunk.

Partes:

- `document.page_content`: texto completo del chunk
- `[:180]`: slicing, toma solo los primeros 180 caracteres
- `.replace("\n", " ")`: reemplaza saltos de linea por espacios

Por que se hace esto:

- para mostrar una vista previa corta y limpia en consola

#### `}`

Cierra el diccionario.

#### `for document in retrieved_docs`

Parte final de la list comprehension.

Que significa:

- "haz ese diccionario para cada documento recuperado"

#### `]`

Cierra la list comprehension.

Resultado final:

- `sources` termina siendo una lista de diccionarios

#### `return RagAnswer(answer=answer, sources=sources)`

Devuelve una instancia de `RagAnswer`.

Por que no devolver un diccionario simple:

- una dataclass deja mas claro el contrato de salida
- mejora legibilidad y estructura

### Resumen conceptual de `pipeline.py`

Este archivo hace dos grandes cosas:

1. Indexacion
   - cargar PDF
   - dividir chunks
   - crear vector store

2. Consulta
   - buscar chunks similares
   - armar contexto
   - ejecutar prompt + modelo
   - devolver respuesta y fuentes

### Explicacion corta de los simbolos que mas te pueden preguntar

#### `[]`

Puede significar dos cosas segun el contexto:

- crear una lista real: `[]`
- indicar tipos genericos: `list[str]`, `list[Document]`

#### `{}`

Crea un diccionario:

```python
{"question": question, "context": context}
```

#### `:`

Puede significar varias cosas:

- anotacion de tipo: `answer: str`
- separar clave y valor en diccionarios: `"page": value`
- inicio de bloque en funciones, clases, `if`, `for`

#### `|`

En LCEL significa componer pasos de una chain.

#### `=`

Asigna un valor a una variable.

### Speech tecnico corto para `pipeline.py`

> `pipeline.py` es el nucleo de RAG. Aqui separo dos fases: indexacion y consulta. En indexacion cargo el PDF, lo divido en chunks y construyo un vector store con embeddings. En consulta recibo una pregunta, recupero los fragmentos semanticamente mas parecidos, los convierto en contexto y luego ejecuto una chain de LangChain compuesta por prompt, modelo y parser. El resultado es una respuesta basada en el documento y acompanada por sus fuentes.

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

### Codigo actual

```python
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
```

### Explicacion linea por linea

#### `from app.core.config import PDF_PATH`

Importa la ruta configurada del PDF.

Por que se usa:

- `main.py` necesita saber que documento cargar
- no hardcodea la ruta directamente

#### `from app.rag.pipeline import ( ... )`

Importa funciones del pipeline.

Por que se usa este bloque:

- `ask_question`: para consultar
- `build_vector_store`: para indexar embeddings
- `load_pdf_documents`: para leer el PDF
- `split_documents`: para fragmentar el contenido

Por que usar parentesis:

- permite partir el import en varias lineas
- mejora legibilidad

#### Linea en blanco

Separa imports de funciones.

#### `def main() -> None:`

Define la funcion principal del programa.

Por que `-> None`:

- indica que no devuelve valor
- solo ejecuta el flujo de la aplicacion

#### `print("Cargando PDF...")`

Muestra mensaje al usuario.

Por que se usa:

- en una demo en vivo necesitas feedback visible

#### `documents = load_pdf_documents(PDF_PATH)`

Carga el PDF y guarda el resultado en `documents`.

Por que `documents`:

- describe claramente que ahora tienes documentos LangChain

#### `print(f"Paginas cargadas: {len(documents)}")`

Muestra cuantas paginas se cargaron.

Partes:

- `f"..."`: f-string
- `len(documents)`: numero de elementos en la lista

Por que sirve:

- confirma que el loader funciono
- da confianza visual al publico

#### `print("Dividiendo documento en chunks...")`

Anuncia la siguiente fase del flujo.

#### `chunks = split_documents(documents)`

Divide los documentos y guarda el resultado en `chunks`.

Por que `chunks`:

- despues de esta linea ya no trabajas con paginas completas, sino con fragmentos

#### `print(f"Chunks creados: {len(chunks)}")`

Muestra cuantos fragmentos se generaron.

Por que sirve:

- hace visible el efecto del chunking

#### `print("Creando embeddings e indexando en memoria...")`

Anuncia la fase de vectorizacion.

#### `vector_store = build_vector_store(chunks)`

Crea el vector store.

Por que `vector_store`:

- deja claro que esta variable representa la base de busqueda semantica

#### `print("Listo. Escribe una pregunta sobre el PDF.")`

Indica al usuario que la indexacion termino.

#### `print("Escribe 'salir' para terminar.\n")`

Da una instruccion de salida.

Por que `\n`:

- deja un espacio visual en consola

#### `while True:`

Empieza un bucle infinito.

Por que se usa:

- queremos permitir varias preguntas
- el programa solo termina cuando el usuario lo decida

#### `question = input("Pregunta: ").strip()`

Lee la entrada del usuario.

Partes:

- `input("Pregunta: ")`: muestra prompt y espera texto
- `.strip()`: elimina espacios al inicio y al final

Por que `.strip()`:

- evita problemas con entradas vacias como `"   "`

#### `if not question:`

Valida si la entrada quedo vacia.

Por que `not question`:

- en Python un string vacio se evalua como falso

#### `continue`

Salta a la siguiente iteracion del bucle.

Por que se usa:

- evita procesar preguntas vacias

#### `if question.lower() in {"salir", "exit", "quit"}:`

Comprueba si el usuario quiere salir.

Partes:

- `.lower()`: convierte a minusculas
- `in {...}`: revisa pertenencia dentro de un conjunto

Por que `{}` aqui:

- en este caso las llaves crean un `set`
- sirve para comprobar si el valor esta entre varias opciones

#### `print("Sesion finalizada.")`

Muestra mensaje de cierre.

#### `break`

Rompe el bucle `while`.

Por que se usa:

- termina el programa de forma controlada

#### `result = ask_question(vector_store, question)`

Llama a la funcion principal de consulta.

Por que guardar en `result`:

- luego se accede a `answer` y `sources`

#### `print("\nRespuesta:\n")`

Imprime un encabezado con saltos de linea.

#### `print(result.answer)`

Imprime la respuesta del modelo.

#### `print("\nFuentes:")`

Imprime encabezado de fuentes.

#### `for source in result.sources:`

Recorre las fuentes recuperadas.

Por que `result.sources`:

- `RagAnswer` devuelve una lista de fuentes junto a la respuesta

#### `page = source["page"]`

Accede al valor asociado a la clave `"page"` del diccionario.

Por que `["page"]`:

- en diccionarios los corchetes sirven para acceder por clave

#### `page_label = page + 1 if isinstance(page, int) else "desconocida"`

Convierte el numero de pagina interno a formato humano.

#### `print(f"- pagina {page_label}: {source['preview']}")`

Imprime una fuente.

Partes:

- `source['preview']`: accede al fragmento corto
- se usan comillas simples dentro porque el f-string externo usa comillas dobles

#### `print()`

Imprime una linea en blanco.

Por que sirve:

- separa visualmente cada respuesta

#### `if __name__ == "__main__":`

Es el patron clasico de entrada en Python.

Que significa:

- si ejecutas este archivo directamente, corre `main()`
- si lo importas desde otro archivo, no lo ejecuta automaticamente

#### `main()`

Llama a la funcion principal.

### Resumen conceptual de `main.py`

`main.py` no implementa RAG. `main.py` usa RAG.

Su trabajo es:

- iniciar el flujo
- mostrar estados al usuario
- capturar preguntas
- imprimir resultados

### Speech tecnico corto para `main.py`

> `main.py` es el punto de entrada de la demo. Mantengo este archivo lo mas liviano posible: carga el PDF, genera los chunks, crea el vector store y luego entra en un loop interactivo para hacer preguntas. Toda la logica real vive en el pipeline; aqui solo orquesto la ejecucion y la salida por consola.

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
