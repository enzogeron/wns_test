import re
from typing import Optional

_MONEY_RE = re.compile(r"[^\d,\.]")


def parse_money(value) -> Optional[float]:
    """
    Convierte distintos formatos reales de dinero a float
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if not s:
        return None

    s = _MONEY_RE.sub("", s)
    if not s:
        return None

    # 6.800 -> 6800
    if s.count(".") >= 1 and s.count(",") == 0:
        s = s.replace(".", "")

    # 1.234,56 -> 1234.56
    if "," in s:
        s = s.replace(".", "").replace(",", ".")

    try:
        return float(s)
    except ValueError:
        return None