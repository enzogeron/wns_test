from app.db.models import Price
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PriceRepository:
    async def upsert_price(
        self,
        session: AsyncSession,
        raw: str,
        norm: str,
        ars_per_kg: float,
    ):
        res = await session.execute(
            select(Price).where(Price.item_name_norm == norm)
        )
        item = res.scalar_one_or_none()

        if item:
            item.item_name_raw = raw
            item.ars_per_kg = ars_per_kg
            return item

        item = Price(
            item_name_raw=raw,
            item_name_norm=norm,
            ars_per_kg=ars_per_kg,
        )
        session.add(item)
        return item