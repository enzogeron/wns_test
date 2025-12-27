from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.services.quote_service import QuoteService

router = APIRouter()
service = QuoteService()

@router.get("/quote")
async def quote(
    recipe_id: int = Query(..., ge=1),
    date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await service.quote_by_recipe_id(session, recipe_id, date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    