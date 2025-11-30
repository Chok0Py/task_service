import pytest
from app.schemas.task import TaskPriority, TaskStatus


def test_create_task(client, prepare_db):
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Integration test task"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Integration test task"
    assert data["priority"] == TaskPriority.MEDIUM.value
    assert data["status"] == TaskStatus.PENDING.value


def test_list_tasks(client, prepare_db):
    client.post("/api/v1/tasks", json={"title": "Task 1", "description": "desc 1"})
    client.post("/api/v1/tasks", json={"title": "Task 2", "description": "desc 2"})

    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "Task 1" in titles
    assert "Task 2" in titles


def test_get_task(client, prepare_db):
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "Get task", "description": "desc"}
    )
    task_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get task"


def test_cancel_task(client, prepare_db):
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "Cancel task", "description": "desc"}
    )
    task_id = create_resp.json()["id"]

    cancel_resp = client.delete(f"/api/v1/tasks/{task_id}")
    assert cancel_resp.status_code == 200
    data = cancel_resp.json()
    assert data["status"] == TaskStatus.CANCELLED.value


def test_task_status(client, prepare_db):
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "Status task", "description": "desc"}
    )
    task_id = create_resp.json()["id"]

    status_resp = client.get(f"/api/v1/tasks/{task_id}/status")
    assert status_resp.status_code == 200
    data = status_resp.json()
    assert data["status"] in [status.value for status in TaskStatus]