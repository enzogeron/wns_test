from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.prices import router as prices_router
from app.api.routes.recipe_ingredients import router as recipe_ingredients_router
from app.api.routes.recipes import router as recipes_router
from app.db.init_db import init_db

app = FastAPI(title="WNS Test API")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(recipes_router)
app.include_router(recipe_ingredients_router)
app.include_router(prices_router)