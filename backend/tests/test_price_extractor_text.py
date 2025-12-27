from app.core.extraction.price_extractor_text import extract_prices_from_pdf_text
from app.core.parsing.pdf_parser import PDFTextDocument
from app.core.parsing.types import DocumentMeta, PageText


def make_pdf_doc(pages):
    return PDFTextDocument(
        meta=DocumentMeta(
            source_name="verduleria.pdf",
            source_path="N/A",
            parser="PDFTextParser"
        ),
        pages=[
            PageText(page_number=i, text=text)
            for i, text in enumerate(pages)
        ]
    )


def test_extract_prices_from_pdf_lines():
    doc = make_pdf_doc([
        "Tomate $1.200\nLechuga $800\n",
        "Zanahoria $950\n",
    ])

    items = extract_prices_from_pdf_text(doc)
    by_name = {i.item_raw: i.cost_per_kg for i in items}

    assert by_name["Tomate"] == 1200
    assert by_name["Lechuga"] == 800
    assert by_name["Zanahoria"] == 950