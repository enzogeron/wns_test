import os

from app.config import settings


def recipes_markdown_path() -> str:
    return os.path.join(settings.input_dir, settings.recipes_markdown)

def produce_prices_pdf_path() -> str:
    return os.path.join(settings.input_dir, settings.produce_prices_pdf)

def meat_fish_prices_xlsx_path() -> str:
    return os.path.join(settings.input_dir, settings.meat_fish_prices_xlsx)