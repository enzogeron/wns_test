from typing import Dict, List

from app.core.extraction.domain_models import PriceItem
from app.core.normalization.text_normalizer import normalize_text
from app.core.parsing.excel_parser import ExcelDocument
from app.core.parsing_utils.money import parse_money
from app.core.parsing_utils.text import is_skippable_text


def extract_prices_from_excel_tables(xlsx_doc: ExcelDocument) -> List[PriceItem]:
    """
    Extrae precios desde un .xlsx

    Estrategia general:
    - No asumimos columnas fijas
    - Recorremos todas las filas y todas las celdas
    - Cuando encontramos una celda de texto que parece un nombre de producto,
      buscamos hacia la derecha un valor que parezca un precio
    - Normalizamos el nombre para evitar duplicados
    """

    # Lista final de precios extraídos
    out: List[PriceItem] = []

    seen: Dict[str, bool] = {}

    for table in xlsx_doc.tables:

        # Recorremos cada fila de la hoja
        for r_idx, row in enumerate(table.rows):

            # Convertimos la fila a lista para asegurar indexación segura
            cells = list(row)

            # Recorremos cada celda de la fila
            for i, cell in enumerate(cells):

                if not isinstance(cell, str):
                    continue

                name_raw = cell.strip()

                if is_skippable_text(name_raw):
                    continue

                # Buscamos un precio "cercano" hacia la derecha.
                # Esto refleja cómo suelen estar armados los excels:
                # [Producto] [Precio] o [Producto] [] [Precio]
                price_val = None
                for j in range(i + 1, min(i + 4, len(cells))):
                    p = parse_money(cells[j])
                    if p is not None:
                        price_val = p
                        break

                # Si no encontramos un precio, descartamos este candidato
                if price_val is None:
                    continue

                # Normalizamos el nombre
                norm = normalize_text(name_raw)
                if not norm or norm in seen:
                    continue

                # Marcamos el producto como ya procesado
                seen[norm] = True

                # Agregamos el precio extraído
                out.append(
                    PriceItem(
                        item_raw=name_raw,
                        cost_per_kg=price_val
                    )
                )

    return out