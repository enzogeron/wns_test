
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.clients.usd_exchange_client import UsdExchangeClient
from app.core.utils.date import validate_date_last_30_days
from app.core.utils.price import calculate_quantity_buy
from app.repositories.price_repo import PriceRepository
from app.repositories.recipe_repo import RecipeRepository


class QuoteService:
    def __init__(self):
        self.recipes = RecipeRepository()
        self.prices = PriceRepository()
        self.usd_exchange = UsdExchangeClient()

    
    async def quote_by_recipe_id(self, session: AsyncSession, recipe_id: int, date_str: str) -> dict:
        """
        Flujo general:
        1. Validar fecha (últimos 30 días)
        2. Obtener receta e ingredientes
        3. Para cada ingrediente:
           - Calcular cantidad a comprar
           - Buscar precio
           - Calcular costo parcial
        4. Calcular totales en ARS y USD
        """
        validate_date_last_30_days(date_str)

        recipe = await self.recipes.get_recipe_by_id(session, recipe_id)
        if not recipe:
            raise ValueError("recipe not found")

        ingredients = await self.recipes.list_ingredients(session, recipe_id)

        items = []
        missing = []
        total_ars = 0.0

        for ing in ingredients:
            required_g = float(ing.required_g or 0)
            buy_g = calculate_quantity_buy(required_g)

            # Buscar precio por nombre normalizado
            price = await self.prices.get_by_norm(session, ing.ingredient_name_norm)
            if not price:
                missing.append(ing.ingredient_name_norm)
                continue

            cost_per_kg = float(price.cost_per_kg)

            # Costo parcial del ingrediente
            cost_ars = (buy_g / 1000) * cost_per_kg
            total_ars += cost_ars

            items.append({
                "name_raw": ing.ingredient_name_raw,
                "name_norm": ing.ingredient_name_norm,
                "required_g": required_g,
                "buy_g": buy_g,
                "cost_per_kg": cost_per_kg,
                "cost_ars": cost_ars,
            })

        # Obtener tipo de cambio USD/ARS para la fecha indicada
        usd_to_ars = await self.usd_exchange.usd_to_ars(date_str)

        # Calcular total en dolares
        total_usd = total_ars / usd_to_ars if usd_to_ars else 0

        return {
            "recipe_id": recipe.id,
            "recipe_name": recipe.name,
            "instructions": recipe.instructions,
            "items": items,
            "date": date_str,
            "total_ars": total_ars,
            "total_usd": total_usd,
            "usd_to_ars": usd_to_ars,
        }