
from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.task import TaskCreate, TaskRead, TaskPriority, TaskStatus


def test_taskcreate_schema_defaults():
    data = {
        "title": "Test task",
        "description": "Unit test description"
    }
    task = TaskCreate.model_validate(data)
    assert task.title == "Test task"
    assert task.description == "Unit test description"
    assert task.priority == TaskPriority.MEDIUM


def test_taskcreate_schema_custom_priority():
    data = {
        "title": "High priority task",
        "description": "Unit test",
        "priority": TaskPriority.HIGH
    }
    task = TaskCreate.model_validate(data)
    assert task.priority == TaskPriority.HIGH


def test_taskread_schema():
    task_id = uuid4()          

    now = datetime.now(timezone.utc)
    data = {
        "id": task_id,         
        "title": "Example",
        "description": "Desc",
        "priority": TaskPriority.HIGH,
        "status": TaskStatus.NEW,
        "created_at": now,
        "started_at": None,
        "finished_at": None,
        "result": None,
        "error": None,
    }
    task = TaskRead.model_validate(data)

    assert task.id == task_id          
    assert task.title == "Example"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.NEW
    assert task.created_at == now