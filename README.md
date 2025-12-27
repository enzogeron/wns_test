# WNS Test - Enzo Geron

## Tools

```
Python -> v3.11.7
FastAPI -> v0.115.6
Node -> v24.11.1
NPM -> v11.6.2
```

## Ejecucion

Se puede ejecutar el backend siguiendo estos pasos

```
cd ./backend
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Se puede ejecutar el frontend siguiendo estos pasos

```
cd ./frontend
npm install

npm run dev
```

## Implementacion

Defini implementar un servicio de preprocesamiento de los datos para que sea mas eficiente y facil la manipulacion de los mismos. Para hacerlo pense en el siguiente flujo:

parsing -> extractors -> normalization -> repositories -> services -> API

parsing: en la carpeta app/core/parsing se implementaron parsers reutilizables para archivos .md, .pdf y .xlsx. La funcion de estos archivos es generar una representacion estructurada 

extractors: en la carpeta app/core/extraction se implementaron los archivos encargados de leer y obtener la informacion de cada uno de los archivos, siguiendo la representacion que genera el proceso de parsing

normalization: el archivo text_normalizer se encagar de normalizar los nombres de ingredientes y productos, para evitar incosistencias antes de que se guarden en la base de datos

repositories: se usa SQLite para persistir los datos ya normalizados y se implementaron 3 modelos Recipe, RecipeIngredient y Price

services: el servicio IngestService contiene toda la logica para que se ejecute el preprocesamiento de los datos

API: estoy usando FastAPI, por lo que cree una API lista para ser consumida por cualquier frontend o CLI
Se expusieron endpoints para:
- ingestión de datos -> POST /ingest
- consulta de recetas -> GET /recipes)
- consulta de ingredientes -> GET /recipes/{recipe_id}/ingredients
- consulta de precios -> GET /prices

## CURLs

Health Check

```
curl http://localhost:8000/health
```

Ingestion de datos

```
curl -X POST http://localhost:8000/ingest
```

Listar recetas

```
curl http://localhost:8000/recipes
```

Obtener receta por ID

```
curl http://localhost:8000/recipes/1
```

Listar precios

```
curl http://localhost:8000/prices
```

Cotizar receta

```
curl "http://localhost:8000/quote?recipe_id=1&date=2025-12-20"
```

## Frontend

Es una app simple desarrollada con Vite, que se encarga de consultar los endpoints /recipes y /quote del backend para mostrar la informacion que necesita el usuario
