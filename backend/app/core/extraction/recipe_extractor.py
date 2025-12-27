from typing import List, Optional

from app.core.extraction.domain_models import IngredientRequirement, Recipe
from app.core.extraction.quantity_parser import (
    parse_quantity_to_grams,
)
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


def extract_recipes(md_doc: MarkdownDocument) -> List[Recipe]:
    """
    Extrae recetas e ingredientes desde un documento .md

    Estrategia general:
    - Cada sección de nivel 1 (#) representa una receta
    - Dentro de cada receta, buscamos subsecciones cuyo título indique que contienen ingredientes
    - Las instrucciones se ignoran
    - Cada linea de ingrediente se parsea teniendo en cuenta los distintos formatos
    """

    # Lista final de recetas extraídas
    recipes: List[Recipe] = []

    # Estado de la receta actual que se está procesando
    current_recipe_name: Optional[str] = None
    current_ingredients: List[IngredientRequirement] = []

    # Flag para saber si estamos dentro de una sección de ingredientes
    in_ingredient_section = False

    # Recorremos todas las secciones del .md en orden
    for sec in md_doc.sections:

        # Si encontramos un header de nivel 1, comienza una nueva receta
        if sec.level == 1:

            if current_recipe_name is not None:
                recipes.append(
                    Recipe(
                        name=current_recipe_name,
                        ingredients=current_ingredients
                    )
                )

            current_recipe_name = sec.title.strip()
            current_ingredients = []
            in_ingredient_section = False
            continue

        # Si aún no se detectó ninguna receta, ignoramos la sección
        if current_recipe_name is None:
            continue

        # Normalizamos el título de la sección para detectar si corresponde a una lista de ingredientes
        title_norm = sec.title.strip().lower()
        in_ingredient_section = title_norm in INGREDIENT_SECTION_TITLES

        if not in_ingredient_section:
            continue

        # Procesamos línea por línea los ingredientes
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
                    source_line=line
                )
            )

    if current_recipe_name is not None:
        recipes.append(
            Recipe(
                name=current_recipe_name,
                ingredients=current_ingredients
            )
        )

    return recipes