from sqlalchemy import Float, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)  # en este challenge alcanza

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (
        UniqueConstraint("recipe_id", "ingredient_name_norm", name="uq_recipe_ingredient"),
        Index("ix_recipe_ing_norm", "ingredient_name_norm"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    ingredient_name_raw: Mapped[str] = mapped_column(String)
    ingredient_name_norm: Mapped[str] = mapped_column(String)
    required_g: Mapped[float] = mapped_column(Float)

class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint("item_name_norm", name="uq_price_item_norm"),
        Index("ix_price_norm", "item_name_norm"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name_raw: Mapped[str] = mapped_column(String, nullable=False)
    item_name_norm: Mapped[str] = mapped_column(String, nullable=False)
    ars_per_kg: Mapped[float] = mapped_column(Float, nullable=False)