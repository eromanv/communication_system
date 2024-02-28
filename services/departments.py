from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import Department

async def read_all_departments(db: AsyncSession):
    async with db as session:
        result = await session.execute(select(Department))
        departments = result.scalars().all()
    if not departments:
        raise HTTPException(status_code=404, detail="No departments found")
    return departments