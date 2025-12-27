from typing import List, Optional

from app.core.extraction.domain_models import IngredientRequirement, Recipe
from app.core.extraction.quantity_parser import parse_quantity_to_grams
from app.core.parsing.markdown_parser import MarkdownDocument
from app.core.parsing_utils.ingredient import (
    clean_prefix,
    extract_ingredient_name,
)

# Titulos de secciones que consideramos como listas de ingredientes
INGREDIENT_SECTION_TITLES = {
    "lista de ingredientes",
    "ingredientes",
    "lista",
}

# Titulos de secciones que consideramos como instrucciones
INSTRUCTION_SECTION_TITLES = {
    "instrucciones",
    "preparación",
    "preparacion",
}


def extract_recipes(md_doc: MarkdownDocument) -> List[Recipe]:
    """
    Extrae recetas, ingredientes e instrucciones desde un documento .md

    Estrategia:
    - Cada sección de nivel 1 (#) representa una receta
    - Las subsecciones indican si contienen ingredientes o instrucciones
    - Los ingredientes se parsean línea por línea
    - Las instrucciones se almacenan como texto libre
    """

    recipes: List[Recipe] = []

    # Estado de la receta actual
    current_recipe_name: Optional[str] = None
    current_ingredients: List[IngredientRequirement] = []
    current_instructions: List[str] = []

    # Flags de contexto
    in_ingredient_section = False
    in_instruction_section = False

    # Recorremos todas las secciones del .md en orden
    for sec in md_doc.sections:

        if sec.level == 1:
            if current_recipe_name is not None:
                recipes.append(
                    Recipe(
                        name=current_recipe_name,
                        ingredients=current_ingredients,
                        instructions="\n".join(current_instructions).strip(),
                    )
                )

            current_recipe_name = sec.title.strip()
            current_ingredients = []
            current_instructions = []
            in_ingredient_section = False
            in_instruction_section = False
            continue

        if current_recipe_name is None:
            continue

        # Normalizamos el título de la sección
        title_norm = sec.title.strip().lower()

        # Detectamos tipo de sección
        in_ingredient_section = title_norm in INGREDIENT_SECTION_TITLES
        in_instruction_section = title_norm in INSTRUCTION_SECTION_TITLES

        if in_ingredient_section:
            for raw_line in sec.lines:
                line = raw_line.strip()
                if not line:
                    continue

                candidate = clean_prefix(line)
                if not candidate:
                    continue

                qty = parse_quantity_to_grams(candidate)
                if qty is None:
                    continue

                name = extract_ingredient_name(candidate)
                if not name:
                    continue

                current_ingredients.append(
                    IngredientRequirement(
                        name_raw=name,
                        required_g=qty.grams,
                        source_line=line,
                    )
                )

        elif in_instruction_section:
            for raw_line in sec.lines:
                line = raw_line.strip()
                if line:
                    current_instructions.append(line)

    if current_recipe_name is not None:
        recipes.append(
            Recipe(
                name=current_recipe_name,
                ingredients=current_ingredients,
                instructions="\n".join(current_instructions).strip(),
            )
        )

    return recipes