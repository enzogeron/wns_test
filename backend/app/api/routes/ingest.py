from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.services.ingest_service import IngestService

router = APIRouter()
service = IngestService()

@router.post("/ingest")
async def ingest(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await service.ingest(session)
    return {"status": "ok", **result}