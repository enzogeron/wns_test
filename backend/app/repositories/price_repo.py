from app.db.models import Price
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PriceRepository:
    async def upsert_price(
        self,
        session: AsyncSession,
        raw: str,
        norm: str,
        cost_per_kg: float,
    ):
        res = await session.execute(
            select(Price).where(Price.item_name_norm == norm)
        )
        item = res.scalar_one_or_none()

        if item:
            item.item_name_raw = raw
            item.cost_per_kg = cost_per_kg
            return item

        item = Price(
            item_name_raw=raw,
            item_name_norm=norm,
            cost_per_kg=cost_per_kg,
        )
        session.add(item)
        return item
    
    async def get_by_norm(self, session: AsyncSession, item_norm: str) -> Price | None:
        res = await session.execute(select(Price).where(Price.item_name_norm == item_norm))
        return res.scalar_one_or_none()