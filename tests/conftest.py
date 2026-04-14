import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import NullPool

from src.main import app
from src.database import get_db, Base

# Тестовая БД
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_task_manager.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
TestAsyncSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

# Переопределяем зависимость get_db для тестов
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# --- Добавляем фикстуру anyio_backend с scope session, чтобы избежать ScopeMismatch ---
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# Создание/удаление таблиц (scope session)
@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

# Асинхронный клиент (scope function по умолчанию)
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac