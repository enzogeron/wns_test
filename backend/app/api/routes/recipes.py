from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.db.models import Recipe

router = APIRouter()

@router.get("/recipes")
async def list_recipes(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Recipe).order_by(Recipe.name))
    recipes = res.scalars().all()
    return [{"id": r.id, "name": r.name} for r in recipes]