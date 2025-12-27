from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.db.models import RecipeIngredient

router = APIRouter()

@router.get("/recipes/{recipe_id}/ingredients")
async def recipe_ingredients(recipe_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute(
        select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)
    )
    items = res.scalars().all()
    return [
        {
            "name_raw": i.ingredient_name_raw,
            "name_norm": i.ingredient_name_norm,
            "required_g": i.required_g,
        }
        for i in items
    ]