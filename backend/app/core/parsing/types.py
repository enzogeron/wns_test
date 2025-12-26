from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class DocumentMeta:
    source_name: str
    source_path: str
    parser: str

@dataclass(frozen=True)
class PageText:
    page_number: int
    text: str

@dataclass(frozen=True)
class SheetTable:
    sheet_name: str
    rows: List[List[Any]]
    meta: Dict[str, Any]
    