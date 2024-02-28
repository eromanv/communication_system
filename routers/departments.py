from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from services.departments import read_all_departments
departments_router = APIRouter(prefix='/departmets', tags=["departments"])

@departments_router.get('/')
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    all_departments = await read_all_departments(db)
    return all_departments