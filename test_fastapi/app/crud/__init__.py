from app.config.database_config import async_engine, Base, engine
import asyncio
from app.models import user_model

# async def create_table():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# def run():
#     loop = asyncio.get_event_loop()
#     tasks = [
#         asyncio.ensure_future( create_table())
#     ]
#     loop.run_until_complete(asyncio.wait(tasks))


