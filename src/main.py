from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import engine, Base
from src.routers import auth_router
from src.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Task Manager API", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "Task Manager API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
