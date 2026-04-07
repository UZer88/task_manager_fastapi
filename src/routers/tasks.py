from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from src.database import get_db
from src.models import User, Task, Tag, TaskStatus, TaskPriority
from src.schemas import TaskCreate, TaskUpdate, TaskResponse
from src.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(
        task_data: TaskCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=current_user.id
    )
    db.add(new_task)
    await db.flush()

    if task_data.tag_ids:
        result = await db.execute(
            select(Tag).where(Tag.id.in_(task_data.tag_ids), Tag.user_id == current_user.id)
        )
        tags = result.scalars().all()
        new_task.tags = tags

    await db.commit()
    await db.refresh(new_task, attribute_names=["tags"])
    return new_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
        status: Optional[TaskStatus] = Query(None),
        priority: Optional[TaskPriority] = Query(None),
        tag_id: Optional[int] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    query = select(Task).where(Task.user_id == current_user.id)

    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if tag_id:
        query = query.join(Task.tags).where(Tag.id == tag_id, Tag.user_id == current_user.id)

    query = query.options(selectinload(Task.tags)).offset(skip).limit(limit)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id).options(selectinload(Task.tags))
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task_data: TaskUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for key, value in update_data.items():
        setattr(task, key, value)

    if task_data.tag_ids is not None:
        tags_result = await db.execute(
            select(Tag).where(Tag.id.in_(task_data.tag_ids), Tag.user_id == current_user.id)
        )
        task.tags = tags_result.scalars().all()

    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task, attribute_names=["tags"])
    return task


@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted"}