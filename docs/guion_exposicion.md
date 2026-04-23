# Guion de Exposicion

Este guion esta pensado para una charla de 60 minutos basada en tu PDF:

`/home/migueldev/Downloads/LangChain Presentation.pdf`

No necesitas memorizarlo palabra por palabra. Usalo como estructura.

## Antes de empezar

Tres ideas para controlar nervios:

1. No intentes sonar perfecto. Intenta sonar claro.
2. Si te equivocas, corriges y sigues. Eso no arruina una charla tecnica.
3. Tu objetivo no es impresionar. Tu objetivo es ensenar un flujo que funcione.

Frase interna util:

> No necesito hacerlo perfecto. Solo necesito llevar al publico de un punto A a un punto B.

## Objetivo de la charla

Tu mensaje principal debe ser:

> Un LLM por si solo no conoce mis datos. Con LangChain puedo conectarlo a mis propios documentos usando RAG.

## Estructura recomendada

### Minuto 0 a 5

Abre simple:

> Hola, soy Eduardo Miguel Muzo. Hoy vamos a construir algo util de verdad: conectar un modelo de IA a nuestros propios datos usando LangChain desde cero.

> En este caso voy a usar un PDF real como fuente de conocimiento, y el objetivo es que podamos hacer preguntas sobre ese documento.

Apoyate en tus slides iniciales:

- problema comun
- LLMs sin contexto privado
- necesidad de un sistema

### Minuto 5 a 10

Explica el problema:

> El problema no es que el modelo sea malo. El problema es que no conoce nuestros datos privados, nuestros procesos ni nuestros documentos internos.

> Entonces la solucion no es solo un modelo mas grande. La solucion es un sistema que pueda buscar informacion relevante en nuestros datos y usarla como contexto.

Frase fuerte:

> Ese sistema se llama RAG: Retrieval Augmented Generation.

### Minuto 10 a 15

Explica el flujo de RAG con palabras simples:

> El flujo es este: primero cargo un documento, luego lo divido en fragmentos, despues convierto esos fragmentos en embeddings, busco los mas relevantes para una pregunta y finalmente el modelo responde usando solo ese contexto.

Si quieres dibujarlo rapido:

`PDF -> chunks -> embeddings -> retrieval -> prompt con contexto -> respuesta`

### Minuto 15 a 20

Conecta con tus slides de LangChain:

> LangChain me ayuda a organizar esto en tres piezas clave: models, prompts y retrieval.

> En mi proyecto eso se refleja asi: una carpeta para configuracion, una para modelos, una para prompts y retrieval, y un archivo principal para ejecutar la demo.

## Parte de codigo en vivo

### Orden exacto para crear archivos

1. `app/core/config.py`
2. `app/llm/providers.py`
3. `app/rag/prompts.py`
4. `app/rag/pipeline.py`
5. `app/main.py`

No cambies ese orden. Ese orden cuenta una historia clara.

## Minuto 20 a 27

### Archivo 1: `app/core/config.py`

Que decir mientras lo escribes:

> Primero voy a separar la configuracion. La API key, el modelo, la ruta del PDF y los parametros de chunking no deben estar mezclados con la logica.

> Esto me permite cambiar configuracion sin tocar el resto del sistema.

Puntos a remarcar:

- `.env`
- ruta del PDF
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `RETRIEVAL_K`

Frase corta:

> Todo lo que cambia por entorno lo saco del codigo duro.

## Minuto 27 a 32

### Archivo 2: `app/llm/providers.py`

Que decir:

> Ahora voy a crear los providers del modelo y de embeddings. En RAG hay dos piezas distintas: el modelo que responde y el modelo que vectoriza texto.

> Eso es importante porque mucha gente cree que un solo modelo hace todo.

Puntos a remarcar:

- `ChatOpenAI`
- `OpenAIEmbeddings`
- mismas credenciales, distinto rol

Frase corta:

> Uno genera respuestas. El otro convierte texto en vectores para buscar significado.

## Minuto 32 a 36

### Archivo 3: `app/rag/prompts.py`

Que decir:

> Aqui defino el comportamiento del sistema. El prompt le dice al modelo que solo puede responder usando el contexto recuperado del PDF.

> Esto ayuda a reducir alucinaciones.

Puntos a remarcar:

- mensaje `system`
- mensaje `human`
- variables `{question}` y `{context}`

Frase corta:

> El prompt no es decoracion. Es una parte central del sistema.

## Minuto 36 a 47

### Archivo 4: `app/rag/pipeline.py`

Esta es la parte central. Baja la velocidad aqui. No corras.

#### `load_pdf_documents()`

Que decir:

> Primero cargo el PDF usando `PyPDFLoader`. Esto me devuelve documentos con metadata por pagina.

#### `split_documents()`

Que decir:

> Luego lo divido en chunks. Esto es importante porque no quiero buscar sobre el PDF completo, sino sobre fragmentos manejables.

#### `build_vector_store()`

Que decir:

> Ahora genero embeddings y los guardo en memoria con `InMemoryVectorStore`.

> Para la charla estoy usando memoria porque es la forma mas simple de entender el concepto. Luego esto se puede mover a PGVector sobre PostgreSQL.

#### `format_context()`

Que decir:

> Cuando recupero fragmentos, necesito convertirlos en un bloque de contexto legible para el modelo.

#### `ask_question()`

Que decir:

> Esta funcion hace la consulta completa: busca, arma contexto, ejecuta la cadena y devuelve respuesta con fuentes.

Cuando llegues a esta linea:

```python
chain = build_qa_prompt() | get_chat_model() | StrOutputParser()
```

di esto:

> Esta linea resume la composicion moderna de LangChain. Primero construyo el prompt, luego lo paso al modelo y al final parseo la salida.

> Aqui ya no estoy llamando al LLM "a mano". Estoy componiendo un pipeline.

## Minuto 47 a 52

### Archivo 5: `app/main.py`

Que decir:

> `main.py` solo orquesta la demo. Carga el PDF una vez, crea el vector store y luego entra en modo interactivo para responder preguntas.

Puntos a remarcar:

- no contiene logica pesada
- se apoya en el pipeline
- despues podria ser reemplazado por FastAPI sin tocar el motor

Frase corta:

> Este archivo es la puerta de entrada, no el cerebro del sistema.

## Minuto 52 a 56

### Ejecuta la demo

Comando:

```bash
uv run python -m app.main
```

Cuando cargue el PDF, di:

> Aqui el sistema esta leyendo mi presentacion, separandola en chunks y creando embeddings.

Luego haz preguntas faciles primero. Por ejemplo:

- `¿Cual es el problema comun que resuelve este enfoque?`
- `¿Que es RAG segun la presentacion?`
- `¿Cuales son los tres pilares de LangChain?`
- `¿Por que LangChain sigue siendo relevante en 2026?`
- `¿Que herramientas se mencionan en la presentacion?`

Haz una pausa despues de cada respuesta y muestra las fuentes.

Frase recomendada:

> Noten que no solo responde, tambien puedo rastrear de que parte del documento salio la respuesta.

## Minuto 56 a 60

### Cierre

Di algo como esto:

> Lo importante aqui no es solo usar un modelo. Lo importante es convertirlo en un sistema que pueda trabajar con nuestros datos.

> Hoy lo hicimos con un PDF y un vector store en memoria. El siguiente paso natural seria persistir embeddings con PGVector o exponer el flujo con FastAPI.

> Pero la idea esencial ya quedo clara: RAG conecta la IA con conocimiento real del negocio.

## Como conectar con tus slides sin chocar con la demo

Tus slides mencionan FastAPI y una ruta web. Como esta demo es mas pequena, usa esta frase:

> En las slides veran una arquitectura mas completa con FastAPI. Para esta sesion en vivo voy a construir primero el nucleo de RAG, porque si se entiende esta parte, luego exponerlo por API es directo.

Si te preguntan por PGVector:

> Hoy estoy usando memoria para hacer visible el concepto. En una aplicacion real, este almacenamiento se moveria a PostgreSQL con PGVector.

## Plan anti-nervios

### Antes de salir

- abre el proyecto antes
- deja `.env` listo
- confirma que el PDF exista
- prueba `uv run python -m app.main`
- ten 3 preguntas preparadas para la demo

### Si te equivocas escribiendo

Di:

> Voy a corregir esta parte un momento.

No pidas disculpas largas. Corrige y sigue.

### Si te quedas en blanco

Vuelve a esta frase:

> Estamos resolviendo un problema simple: el modelo no conoce mis datos, asi que primero recupero contexto y luego respondo.

### Si algo falla en vivo

Ten este cierre de seguridad:

> Aunque aqui falle un detalle de ejecucion, lo importante es el flujo conceptual: cargar, chunking, embeddings, retrieval y respuesta con contexto.

## Frases cortas que te ayudan a sonar claro

- `Voy a separar responsabilidades.`
- `Esto es configuracion, no logica de negocio.`
- `Aqui empieza el flujo de RAG.`
- `Este prompt reduce alucinaciones.`
- `Ahora convierto texto en embeddings.`
- `Recupero fragmentos relevantes, no el PDF entero.`
- `Este archivo orquesta; no concentra inteligencia.`
- `Primero entiendo el concepto, luego escalo la infraestructura.`

## Ultima recomendacion

No intentes demostrar demasiado.

Tu charla va a salir mejor si haces muy bien estas tres cosas:

1. explicas el problema,
2. muestras el flujo de RAG,
3. ejecutas una demo corta que funcione.

Eso basta para una muy buena primera exposicion tecnica.
