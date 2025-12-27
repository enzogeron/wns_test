# WNS Test - Enzo Geron

## Resumen

Este proyecto procesa tres archivos de entrada (recetas en formato .md, precios de productos en .pdf y .xlsx), normaliza los datos y los almacena en SQLite.
Luego, se expone un endpoint final `/quote` que calcula el costo total de una receta para una fecha determinada, aplicando la regla de "comprar múltiplos de 250 gramos" y utilizando la API de tipo de cambio proporcionada.
La interfaz de usuario mínima se realizo en Vite y consume los endpoints `/recipes` - `/quote`.

## Tools

```
Para backend
Python -> v3.11.7
FastAPI -> v0.115.6

Para frontend
Node -> v20.11.1
NPM -> v11.6.2
```

## Ejecucion

Se esta usando Docker para ejecutar de forma facil ambos proyectos

En el mismo directorio donde se encuentra el archivo docker-compose.yml

Ejecutar el comando

```
docker compose up --build

# para ver logs
docker compose logs

# detener servicios
docker compose down
```

Cuando terminen de descargarse las dependencias se deberia ver algo como la siguiente imagen

![alt text](image.png)

Es necesario ejecutar el proceso de ingesta de datos la primera vez para que el frontend tenga informacion que mostrar. Desde la terminal o postman ejecutar:

```
curl -X POST http://localhost:8000/ingest
```

URL Frontend: http://localhost:5173/

Se puede ejecutar el backend de forma manual siguiendo estos pasos

```
cd ./backend
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Se puede ejecutar el frontend de forma manual siguiendo estos pasos

```
cd ./frontend
npm install

npm run dev
```

## Implementacion

Defini implementar un servicio de preprocesamiento de los datos para que sea mas eficiente y facil la manipulacion de los mismos. Para hacerlo pense en el siguiente flujo:

inputs -> parsing -> extractors -> normalization -> repositories (SQLite) -> services -> API -> UI

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

## Asunciones

- Los precios en .pdf/.xlsx se mantienen constantes durante el mes y se redonde al siguiente multiplo de 250g (como se indica en el reto)
- La coincidencia de ingredientes se basa en nombres normalizados (por ejemplo "Morrón" → "morron")

## Limitaciones

- El analisis de PDF depende de la calidad de la extraccion de texto de la libreria `pdfplumber`
- Se utiliza SQLite para simplificar el proceso de ingesta de datos

## Fortalezas y debilidades

- Como fortaleza creo que la arquitectura que implemente de (análisis/extracción/normalización/persistencia/servicios) permite reutilización. Tambien la separación entre la lógica del dominio y los servicios hace  que sea facil realizar modificaciones

- Como debilidad creo que la correspondencia entre ingredientes y precios al basarse en normalización de texto puede no ser lo ideal, por lo que buscaria extender esto a un enfoque mas robusto. En relacion a rendimiento si bien ahora los archivos que se procesan no son muy grandes, creo que deberia considerar este caso para optimizar algunas funciones

## Escalabilidad

Para llevar esta aplicacion a un entorno productivo, cambiaría SQLite por otra base de datos como PostgreSQL, añadiria gestion de migraciones para controlar los cambios que se hacen en la DB. La ingesta de datos me parece que seria mejor que se ejecute como un trabajo en segundo plano en lugar de un endpoint manual

Tambien agregaria autenticación/autorización y gestión centralizada de errores con observabilidad usando un middleware que asigne un request-id a cada solicitud para que sea mas facil buscar errores, por ultimo implementar CI/CD tambien seria muy bueno sobre todo tener mas tests unitarios/integracion