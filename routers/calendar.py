from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from schemas.schemas import TaskOnTheCalendarSchemas, TaskOnTheCalendarSchemasUpdate
from services.calendar import (
    create_event_in_calendar,
    delete_task_by_id,
    finalize_task,
    get_events_in_calendar_by_user_id,
)

calendar = APIRouter(tags=["calendar"], prefix="/calendar")


@calendar.get("/{user_id}")
async def get_calendar_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        calendar = await get_events_in_calendar_by_user_id(user_id, db)
        return calendar
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"detail": error.detail}
        )


@calendar.post("/{user_id}")
async def make_event_in_calendar(
    data: TaskOnTheCalendarSchemas, user_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        event = await create_event_in_calendar(data, user_id, db)
        return {"message added": event}
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"detail": error.detail}
        )


@calendar.patch("/{deal_id}")
async def approve_task(
    deal_id: int,
    approved_dates: TaskOnTheCalendarSchemasUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        updated_task = await finalize_task(deal_id, approved_dates, db)
        return updated_task
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"detail": error.detail}
        )


@calendar.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_task_by_id(task_id, db)
