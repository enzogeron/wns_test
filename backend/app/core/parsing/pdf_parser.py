from dataclasses import dataclass
from typing import List, Optional

import pdfplumber
from app.core.parsing.base import Parser
from app.core.parsing.types import DocumentMeta, PageText


@dataclass(frozen=True)
class PDFTextDocument:
    meta: DocumentMeta
    pages: List[PageText]

class PDFTextParser(Parser[PDFTextDocument]):
    def parse(self, path: str, source_name: Optional[str] = None) -> PDFTextDocument:
        meta = self._meta(path, source_name, "PDFTextParser")

        pages: List[PageText] = []

        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                pages.append(PageText(page_number=i, text=text))

        return PDFTextDocument(meta=meta, pages=pages)