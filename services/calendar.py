from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import TaskOnTheCalendar, User
from sqlalchemy import select
import logging
from schemas.schemas import TaskOnTheCalendarSchemas, TaskOnTheCalendarSchemasUpdate
from services.user import read_user_id


async def create_event_in_calendar(
    data: TaskOnTheCalendarSchemas, user_id: int, db: AsyncSession
):
    """Создать событие в календаре с использованием user_created.id."""
    async with db as session:
        event = TaskOnTheCalendar(
            user_calendar_id=data.user_calendar_id,
            user_created_id=user_id,
            task_name=data.task_name,
            description=data.description,
            date_time_start=data.date_time_start.replace(
                tzinfo=None
            ),  # так решаем проблему с часовым поясом у pydantic
            date_time_end=data.date_time_end.replace(tzinfo=None),
            created_at=datetime.utcnow(),
        )


        try:
            session.add(event)
            await session.flush()
            await session.refresh(event)
            await session.commit()
        except Exception as error:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка: {str(error)}")

    return event



async def get_events_in_calendar_by_user_id(user_calendar_id: int, db: AsyncSession):
    """Получить события конкретного пользователя по user_created_id."""
    async with db as session:
        statement = select(TaskOnTheCalendar).filter_by(
            user_calendar_id=user_calendar_id
        )
        result = await session.execute(statement)
        event = result.scalars().all()
        if event is None:
            raise HTTPException(
                status_code=404,
                detail=f"event with user id {user_calendar_id} is not founded",
            )
    return event


async def finalize_task(
    task_id: int, approved_dates: TaskOnTheCalendarSchemasUpdate, db: AsyncSession
):
    """Финализировать событие PATCH"""
    async with db as session:
        statement = select(TaskOnTheCalendar).filter_by(id=task_id)
        result = await session.execute(statement)
        task = result.scalars().first()

        if task is None:
            return None

        task.task_name = approved_dates.task_name
        task.description = approved_dates.description
        task.date_time_start = approved_dates.date_time_start.replace(tzinfo=None)
        task.date_time_end = approved_dates.date_time_end.replace(tzinfo=None)

        await session.commit()
        await session.refresh(task)

        return task


async def delete_task_by_id(task_id: int, db: AsyncSession):
    """Удалить событие по его ID."""
    async with db as session:
        statement = select(TaskOnTheCalendar).filter_by(id=task_id)
        result = await session.execute(statement)
        task = result.scalars().first()
        logging.info(task)

        if not task:
            raise HTTPException(status_code=404, detail="Нет такой задачи")

        await session.delete(task)
        await session.commit()

        return {"message": "Задача удалена"}
