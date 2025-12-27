import re
from typing import List

from app.core.extraction.domain_models import PriceItem
from app.core.parsing.pdf_parser import PDFTextDocument
from app.core.parsing_utils.money import parse_money

# Regex que detecta líneas del tipo:
# "Tomate $1.200"
# "Lechuga 800"
_PRICE_LINE_RE = re.compile(
    r"^(?P<name>[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+?)\s+\$?\s*(?P<price>\d{1,3}(?:\.\d{3})*)$"
)


def extract_prices_from_pdf_text(
    pdf_doc: PDFTextDocument
) -> List[PriceItem]:
    """
    Extrae precios desde un PDF previamente convertido a texto

    Estrategia general:
    - Recorremos pagina por pagina
    - Dividimos el texto en lineas
    - Aplicamos la expresion regular _PRICE_LINE_RE
    - Convertimos el precio usando una función reutilizable
    """

    # Lista final de precios encontrados
    items: List[PriceItem] = []

    for page in pdf_doc.pages:

        # Extraemos el texto de la página y lo separamos por líneas
        lines = (page.text or "").splitlines()

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Intentamos hacer match contra el patrón esperado
            m = _PRICE_LINE_RE.match(line)
            if not m:
                continue

            name = m.group("name").strip()

            # Extraemos y parseamos el precio
            price = parse_money(m.group("price"))

            # Agregamos el precio extraído
            items.append(
                PriceItem(
                    item_raw=name,
                    cost_per_kg=price
                )
            )

    return items