# tests/test_tasks.py
import pytest
from httpx import AsyncClient


@pytest.fixture
async def auth_token(client: AsyncClient):
    """Фикстура для получения токена авторизации"""
    email = "taskuser@example.com"
    password = "taskpass123"
    await client.post("/auth/register", json={"email": email, "password": password})
    resp = await client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


@pytest.mark.anyio
async def test_create_task(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task_data = {
        "title": "Test task",
        "description": "Some description",
        "status": "pending",
        "priority": "high"
    }
    response = await client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    assert data["priority"] == task_data["priority"]
    assert "id" in data


@pytest.mark.anyio
async def test_get_tasks(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Создадим две задачи
    await client.post("/tasks/", json={"title": "Task 1"}, headers=headers)
    await client.post("/tasks/", json={"title": "Task 2", "priority": "low"}, headers=headers)

    response = await client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 2
    # Проверим фильтрацию по приоритету
    response_low = await client.get("/tasks/?priority=low", headers=headers)
    low_tasks = response_low.json()
    assert all(t["priority"] == "low" for t in low_tasks)


@pytest.mark.anyio
async def test_get_single_task(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_resp = await client.post("/tasks/", json={"title": "Single task"}, headers=headers)
    task_id = create_resp.json()["id"]

    response = await client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Single task"


@pytest.mark.anyio
async def test_update_task(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_resp = await client.post("/tasks/", json={"title": "Old title"}, headers=headers)
    task_id = create_resp.json()["id"]

    update_resp = await client.put(f"/tasks/{task_id}", json={"title": "New title"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New title"


@pytest.mark.anyio
async def test_delete_task(client: AsyncClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_resp = await client.post("/tasks/", json={"title": "To be deleted"}, headers=headers)
    task_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Task deleted"

    # Проверим, что задача действительно удалена
    get_resp = await client.get(f"/tasks/{task_id}", headers=headers)
    assert get_resp.status_code == 404