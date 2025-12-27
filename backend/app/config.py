from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_dir: str = "../inputs"
    
    data_dir: str = "./data"
    db_url: str = "sqlite+aiosqlite:///./data/app.db"

    recipes_markdown: str = "Recetas.md"
    produce_prices_pdf: str = "verduleria.pdf"
    meat_fish_prices_xlsx: str = "Carnes y Pescados.xlsx"


settings = Settings()