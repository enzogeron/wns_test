from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.db.models import Price

router = APIRouter()

@router.get("/prices")
async def list_prices(
    session: AsyncSession = Depends(get_session),
):
    q = select(Price)
    res = await session.execute(q)
    items = res.scalars().all()
    return [
        {
            "item_raw": p.item_name_raw,
            "item_norm": p.item_name_norm,
            "cost_per_kg": p.cost_per_kg,
        }
        for p in items
    ]