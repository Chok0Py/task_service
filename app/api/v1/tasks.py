from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskRead

from app.core.database import SessionLocal

router = APIRouter(prefix="/api/v1", tags=["tasks"])


def _task_to_schema(task: Task) -> TaskRead:
    return TaskRead.model_validate({
        **task.__dict__,
        "priority": task.priority.value,
        "status": task.status.value,
    })


@router.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskCreate):
    async with SessionLocal() as session:
        db_task = Task(
            title=task.title,
            description=task.description or None,
            priority=task.priority or TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
        )
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return _task_to_schema(db_task)


@router.get("/tasks", response_model=list[TaskRead])
async def list_tasks():
    async with SessionLocal() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        return [_task_to_schema(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: UUID):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return _task_to_schema(task)


@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: UUID):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": task.status.value}


@router.delete("/tasks/{task_id}", response_model=TaskRead)
async def cancel_task(task_id: UUID):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.status = TaskStatus.CANCELLED
        await session.commit()
        await session.refresh(task)
        return _task_to_schema(task)