from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class IngredientRequirement:
    name_raw: str
    required_g: Optional[float]
    source_line: str

@dataclass(frozen=True)
class Recipe:
    name: str
    ingredients: List[IngredientRequirement]
    instructions: str = ""

@dataclass(frozen=True)
class PriceItem:
    item_raw: str
    cost_per_kg: float
