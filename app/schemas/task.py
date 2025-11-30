from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class TaskStatus(str, Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str]
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskUpdate(BaseModel):
    status: Optional[TaskStatus]
    result: Optional[str]
    error: Optional[str]


class TaskRead(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    result: Optional[str]
    

    class Config:
        model_config = ConfigDict(from_attributes=True)