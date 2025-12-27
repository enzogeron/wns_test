import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedQuantity:
    grams: float

_QTY_RE = re.compile(r"(?P<num>[\d]+(?:[.,]\d+)?)\s*(?P<unit>kg|g)\b", re.IGNORECASE)

def _to_float(num_str: str) -> float:
    return float(num_str.replace(",", "."))

def parse_quantity_to_grams(text: str) -> Optional[ParsedQuantity]:
    m = _QTY_RE.search(text)
    if not m:
        return None

    qty = _to_float(m.group("num"))
    unit = m.group("unit").lower()

    grams = qty * 1000.0 if unit == "kg" else qty
    return ParsedQuantity(grams=grams)

def remove_quantity_part(text: str) -> str:
    return _QTY_RE.sub("", text, count=1).strip()