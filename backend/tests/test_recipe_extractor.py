from app.core.extraction.recipe_extractor import extract_recipes
from app.core.parsing.markdown_parser import MarkdownDocument, MarkdownSection
from app.core.parsing.types import DocumentMeta


def make_md_doc(sections):
    return MarkdownDocument(
        meta=DocumentMeta(
            source_name="Recetas.md",
            source_path="N/A",
            parser="MarkdownParser"
        ),
        sections=sections
    )


def test_extract_simple_recipe_with_ingredients():
    doc = make_md_doc([
        MarkdownSection(level=1, title="Receta titulo", lines=[]),
        MarkdownSection(level=2, title="Lista de Ingredientes", lines=[
            "- 1 kg de Asado de tira",
            "- 250 g de Tomate",
            "- 400 g de Cebolla",
            "1. Merluza fresca: 1,5 kg",
            "2. Espinaca: 1 kg",
        ]),
    ])

    recipes = extract_recipes(doc)

    assert len(recipes) == 1
    r = recipes[0]
    assert r.name == "Receta titulo"
    assert len(r.ingredients) == 5

    by_name = {i.name_raw: i.required_g for i in r.ingredients}
    assert by_name["Asado de tira"] == 1000
    assert by_name["Tomate"] == 250
    assert by_name["Cebolla"] == 400
    assert by_name["Merluza fresca"] == 1500
    assert by_name["Espinaca"] == 1000