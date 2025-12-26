from fastapi import APIRouter

from app.config import settings
from app.core.parsing.excel_parser import ExcelTableParser
from app.core.parsing.markdown_parser import MarkdownParser
from app.core.parsing.pdf_parser import PDFTextParser
from app.core.utils.input_paths import (
    meat_fish_prices_xlsx_path,
    produce_prices_pdf_path,
    recipes_markdown_path,
)

router = APIRouter()

@router.get("/ingest/preview")
def ingest_preview():
    md_doc = MarkdownParser().parse(recipes_markdown_path(), settings.recipes_markdown)
    pdf_doc = PDFTextParser().parse(produce_prices_pdf_path(), settings.produce_prices_pdf)
    xlsx_doc = ExcelTableParser().parse(meat_fish_prices_xlsx_path(), settings.meat_fish_prices_xlsx)

    return {
        "markdown": {
            "meta": md_doc.meta.__dict__,
            "sections_sample": [
                {"level": s.level, "title": s.title, "lines_count": len(s.lines)}
                for s in md_doc.sections[:80]
            ],
            "sections_count": len(md_doc.sections),
        },
        "pdf": {
            "meta": pdf_doc.meta.__dict__,
            "pages_count": len(pdf_doc.pages),
            "page_text_preview": [
                {"page": p.page_number, "chars": len(p.text)}
                for p in pdf_doc.pages
            ],
        },
        "xlsx": {
            "meta": xlsx_doc.meta.__dict__,
            "sheets": [
                {"sheet_name": t.sheet_name, "rows": t.meta["rows"], "max_cols": t.meta["max_cols"]}
                for t in xlsx_doc.tables
            ],
        },
    }
