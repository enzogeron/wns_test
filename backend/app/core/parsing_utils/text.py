SKIP_TITLES = {
    "carnicería", "carniceria",
    "pescadería", "pescaderia",
    "carne vacuna", "carne de cerdo", "pollo",
    "corte", "tipo",
    "precio (ars/kg)", "precio", "precio(ars/kg)"
}


def is_skippable_text(s: str) -> bool:
    """
    Determina si un texto corresponde a headers, títulos o filas de relleno que deben ignorarse
    """
    low = (s or "").strip().lower()

    if not low:
        return True

    if low in SKIP_TITLES:
        return True

    if low == "precio" or "ars/kg" in low:
        return True

    return False