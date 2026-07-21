






import asyncio
from app.celery_app import celery_app
from app.sync import sync_daily_stats
from app.database import async_session



@celery_app.task
def run_sync_daily_stats_task():
    async def async_runner():
        async with async_session() as db:
            await sync_daily_stats(db)
    asyncio.run(async_runner())