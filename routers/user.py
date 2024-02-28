from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import user
from dependencies import get_db
from schemas.schemas import UserSchemas, UpdateUser
from services.user import create_user, read_user_id, change_user, make_user_not_active, read_user_all
from models.models import User

routes = APIRouter(prefix="/users", tags=["user"])


@routes.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    user = await read_user_all(db)
    return user


@routes.post("/", tags=["user"])
async def create_user_endpoint(data: UserSchemas, db: AsyncSession = Depends(get_db)):
    try:
        user = await create_user(data, db)
        return user
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@routes.get("/{user_id}", tags=["user"])
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await read_user_id(user_id, db)
        return user
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"detail": error.detail}
        )


@routes.put("/{user_id}", tags=["user"])
async def update_user(
    data: UpdateUser, user_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        user = await change_user(data, user_id, db)
        return user
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@routes.put("/change_act/{user_id}", tags=["user_role"])
async def change_user_active(
    is_active: bool, user_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        user = await make_user_not_active(is_active, user_id, db)
        return user
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
