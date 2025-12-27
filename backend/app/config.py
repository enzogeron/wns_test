from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_origins: list[str] = ["http://localhost:5173"]
    input_dir: str = "../inputs"
    text_encoding: str = "utf-8"

    data_dir: str = "./data"
    db_url: str = "sqlite+aiosqlite:///./data/app.db"

    recipes_markdown: str = "Recetas.md"
    produce_prices_pdf: str = "verduleria.pdf"
    meat_fish_prices_xlsx: str = "Carnes y Pescados.xlsx"


settings = Settings()