from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.extraction.price_extractor_table import extract_prices_from_excel_tables
from app.core.extraction.price_extractor_text import extract_prices_from_pdf_text
from app.core.extraction.recipe_extractor import extract_recipes
from app.core.normalization.text_normalizer import normalize_text
from app.core.parsing.excel_parser import ExcelTableParser
from app.core.parsing.markdown_parser import MarkdownParser
from app.core.parsing.pdf_parser import PDFTextParser
from app.core.utils.input_paths import (
    meat_fish_prices_xlsx_path,
    produce_prices_pdf_path,
    recipes_markdown_path,
)
from app.db.models import RecipeIngredient
from app.repositories.price_repo import PriceRepository
from app.repositories.recipe_repo import RecipeRepository


class IngestService:
    def __init__(self):
        self.recipes_parser = MarkdownParser()
        self.pdf_parser = PDFTextParser()
        self.xlsx_parser = ExcelTableParser()
        self.recipe_repo = RecipeRepository()
        self.price_repo = PriceRepository()

    async def ingest(self, session: AsyncSession):
        md_doc = self.recipes_parser.parse(recipes_markdown_path(), source_name=settings.recipes_markdown)
        pdf_doc = self.pdf_parser.parse(produce_prices_pdf_path(), source_name=settings.produce_prices_pdf)
        xlsx_doc = self.xlsx_parser.parse(meat_fish_prices_xlsx_path(), source_name=settings.meat_fish_prices_xlsx)

        recipes = extract_recipes(md_doc)
        produce_prices = extract_prices_from_pdf_text(pdf_doc)
        xlsx_prices = extract_prices_from_excel_tables(xlsx_doc)

        recipes_count = 0
        ingredients_count = 0
        prices_count = 0

        for r in recipes:
            recipe = await self.recipe_repo.upsert_recipe(session, r.name)
            recipes_count += 1

            ing_entities = []
            for ing in r.ingredients:
                norm = normalize_text(ing.name_raw)
                ing_entities.append(
                    RecipeIngredient(
                        recipe_id=recipe.id,
                        ingredient_name_raw=ing.name_raw,
                        ingredient_name_norm=norm,
                        required_g=float(ing.required_g or 0),
                    )
                )
            await self.recipe_repo.replace_ingredients(session, recipe.id, ing_entities)
            ingredients_count += len(ing_entities)

        for p in produce_prices:
            norm = normalize_text(p.item_raw)
            await self.price_repo.upsert_price(session, p.item_raw, norm, p.ars_per_kg)
            prices_count += 1

        for p in xlsx_prices:
            norm = normalize_text(p.item_raw)
            await self.price_repo.upsert_price(session, p.item_raw, norm, p.ars_per_kg)
            prices_count += 1

        return {
            "recipes_count": recipes_count,
            "ingredients_count": ingredients_count,
            "prices_count": prices_count,
        }