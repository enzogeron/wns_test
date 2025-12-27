import re

from app.core.extraction.quantity_parser import (
    parse_quantity_to_grams,
    remove_quantity_part,
)

_PREFIX_RE = re.compile(r"^(\s*[-*]\s+|\s*\d+\.\s+|\s*[a-zA-Z]\.\s+)\s*")


def clean_prefix(line: str) -> str:
    """
    Elimina bullets, numeraciones o letras
    """
    return _PREFIX_RE.sub("", line.strip()).strip()


def extract_ingredient_name(line_no_prefix: str) -> str:
    """
    Extrae el nombre del ingrediente desde formatos como:
    - "Merluza fresca: 1,5 kg"
    """
    if ":" in line_no_prefix:
        left, right = line_no_prefix.split(":", 1)
        if parse_quantity_to_grams(right) is not None:
            return left.strip()
        if parse_quantity_to_grams(left) is not None:
            return right.strip()

    name = remove_quantity_part(line_no_prefix)
    return re.sub(r"^\s*de\s+", "", name, flags=re.IGNORECASE).strip()