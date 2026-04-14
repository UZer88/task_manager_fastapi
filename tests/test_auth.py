import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "strongpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data

@pytest.mark.anyio
async def test_register_duplicate_email(client: AsyncClient):
    # Первая регистрация
    await client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "pass123"
    })
    # Вторая регистрация с тем же email
    response = await client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "pass456"
    })
    assert response.status_code == 400
    assert "already registered" in response.text.lower()

@pytest.mark.anyio
async def test_login_success(client: AsyncClient):
    # Сначала регистрируем пользователя
    await client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "secretpass"
    })
    # Логинимся
    response = await client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "secretpass"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.anyio
async def test_login_wrong_password(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "correctpass"
    })
    response = await client.post(
        "/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert "incorrect" in response.text.lower()