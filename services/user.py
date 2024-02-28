from datetime import datetime
from fastapi import HTTPException
from models.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import UserSchemas, UpdateUser


async def read_user_id(id: int, db: AsyncSession):
    async with db as session:
        user = await session.get(User, id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"user {id} is not founded")
    return user


async def read_user_all(db: AsyncSession):
    async with db as session:
        statement = select(User)
        result = await session.execute(statement)
        users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


async def create_user(data: UserSchemas, db: AsyncSession):
    user = User(
        email=data.email,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_verified=data.is_verified,
        hashed_password=data.hashed_password,
        is_active=data.is_active,
        is_superuser=data.is_superuser,
        role_id=data.role_id,
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Some error while adding the info to the database, {str(error)}",
        )
    return user


async def change_user(data: UpdateUser, id: int, db: AsyncSession):
    async with db as session:
        user = await session.get(User, id)
        try:
            if user:
                user.email = data.email
                user.is_verified = data.is_verified
                user.is_active = data.is_active
                user.is_superuser = data.is_superuser
                user.role_id = data.role_id
                await db.commit()
                await db.refresh(user)
                return user
            else:
                raise HTTPException(status_code=404, detail="No user founded")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"wrong update: {str(e)}")


async def make_user_not_active(is_active: bool, id: int, db: AsyncSession):
    async with db as session:
        user = await session.get(User, id)
        try:
            if user:
                user.is_active = is_active
                await db.commit()
                await db.refresh(user)
                return user
            raise HTTPException(status_code=404, detail="No user founded")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"wrong update: {str(e)}")
