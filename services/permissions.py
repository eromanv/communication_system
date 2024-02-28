from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Permission
from schemas.schemas import Permission as PermissionSchema
from models.models import Permission


async def get_all_permissions(db: AsyncSession):
    async with db as session:
        permissions = await session.execute(select(Permission))
        return permissions.scalars().all()


