from app.core.extraction.price_extractor_table import extract_prices_from_excel_tables
from app.core.parsing.excel_parser import ExcelDocument
from app.core.parsing.types import DocumentMeta, SheetTable


def make_excel_doc(rows):
    return ExcelDocument(
        meta=DocumentMeta(
            source_name="test.xlsx",
            source_path="N/A",
            parser="ExcelTableParser"
        ),
        tables=[
            SheetTable(
                sheet_name="Sheet1",
                rows=rows,
                meta={"rows": len(rows), "max_cols": max(len(r) for r in rows)}
            )
        ],
    )


def test_extract_prices_from_multiple_columns():
    rows = [
        ["Corte", "Precio (ARS/kg)", "", "", "Tipo", "Precio"],
        ["Asado de tira", "$ 6.800", "", "", "Merluza fresca", "$ 5.000"],
        ["Pechuga", "3.800", "", "", "Pejerrey", "6500"],
    ]

    doc = make_excel_doc(rows)
    items = extract_prices_from_excel_tables(doc)

    names = sorted(i.item_raw for i in items)
    print(names)
    assert names == [
        "Asado de tira",
        "Merluza fresca",
        "Pechuga",
        "Pejerrey",
    ]

    prices = {i.item_raw: i.ars_per_kg for i in items}
    assert prices["Asado de tira"] == 6800
    assert prices["Merluza fresca"] == 5000
    assert prices["Pechuga"] == 3800
    assert prices["Pejerrey"] == 6500


def test_excel_extractor_skips_headers_and_titles():
    rows = [
        ["Carnicería", "", "", "", "Pescadería", ""],
        ["Corte", "Precio", "", "", "Tipo", "Precio"],
        ["Asado de tira", "6800", "", "", "Merluza fresca", "5000"],
    ]

    doc = make_excel_doc(rows)
    items = extract_prices_from_excel_tables(doc)

    names = [i.item_raw for i in items]

    assert "Carnicería" not in names
    assert "Corte" not in names
    assert names == [
        "Asado de tira",
        "Merluza fresca",
    ]
