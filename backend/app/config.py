from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_dir: str = "../inputs"

    recipes_markdown: str = "Recetas.md"
    produce_prices_pdf: str = "verduleria.pdf"
    meat_fish_prices_xlsx: str = "Carnes y Pescados.xlsx"


settings = Settings()