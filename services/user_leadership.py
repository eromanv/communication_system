from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import UserLeadership

async def get_all_records(db: AsyncSession):
    async with db as session:
        records = await session.execute(select(UserLeadership))
        result = records.scalar.all()
    if not result:
        raise HTTPException(status_code=404, detail="No records found")
    return result


async def get_record_by_user_id(id: int, db: AsyncSession):
    pass

async def create_new_record(id: int, is_subordinate: int, data: UserLeadershipSchemas, db: AsyncSession):
    async with db as session:
        record = UserLeadership(
            user_id = id,
            is_subordinated_id = is_subordinate,
            is_head_id = data.is_head_id,
            position_name = data.postion_name,

        )


async def delete_record(id: int, db: AsyncSession):
    pass

