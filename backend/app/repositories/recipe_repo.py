from app.db.models import Recipe, RecipeIngredient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeRepository:
    async def upsert_recipe(self, session: AsyncSession, name: str) -> Recipe:
        res = await session.execute(select(Recipe).where(Recipe.name == name))
        recipe = res.scalar_one_or_none()
        if recipe:
            return recipe

        recipe = Recipe(name=name)
        session.add(recipe)
        await session.flush()
        return recipe

    async def replace_ingredients(self, session: AsyncSession, recipe_id: int, ingredients: list[RecipeIngredient]):
        await session.execute(delete(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id))
        for ing in ingredients:
            session.add(ing)