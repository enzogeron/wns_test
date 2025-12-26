from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.preview import router as ingest_preview_router

app = FastAPI(title="WNS Test API")
app.include_router(health_router)
app.include_router(ingest_preview_router)