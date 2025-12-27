import os

from app.config import settings
from app.db.models import Base
from app.db.session import engine


async def init_db():
    os.makedirs(settings.data_dir, exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)