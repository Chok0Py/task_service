import random
from datetime import datetime
from sqlalchemy import select
from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.task import Task, TaskStatus


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
async def execute_task(self, task_id: str):
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()
            if not task or task.status != TaskStatus.PENDING:
                return

            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.utcnow()
            await session.commit()
        
        await asyncio.sleep(random.uniform(5, 15))
        
        if random.random() < 0.2:
            task.status = TaskStatus.FAILED
            task.finished_at = datetime.utcnow()
            task.error_info = "Случайная ошибка при выполнении задачи!"
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    await session.merge(task)
                    await session.commit()
            raise Exception(task.error_info)

        task.status = TaskStatus.COMPLETED
        task.finished_at = datetime.utcnow()
        task.result = f"Задача выполнена успешно! Случайное число: {random.randint(1, 1000)}"
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.merge(task)
                await session.commit()


@celery_app.task
async def process_pending_tasks():

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Task).where(Task.status == TaskStatus.PENDING)
        )
        pending_tasks = result.scalars().all()

        for task in pending_tasks:
            await execute_task.delay(str(task.id))