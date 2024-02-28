from typing import List
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from models.models import Permission, Role, role_permissions
from schemas.schemas import RoleSchemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_role(role_data: RoleSchemas, permissions: List[str], db: AsyncSession):
    async with db as session:

        existing_role = await session.execute(select(Role).where(Role.role_name == role_data.role_name))
        existing_role_obj = existing_role.scalar()

        if existing_role_obj:
            raise HTTPException(status_code=400, detail=f"Role '{role_data.role_name}' already exists.")
        
        role = Role(role_name=role_data.role_name)

        for permission_name in permissions:
            permission = await session.execute(select(Permission).where(Permission.permission_type == permission_name))
            permission_obj = permission.scalar()

            if not permission_obj:
                raise HTTPException(status_code=400, detail=f"Permission '{permission_name}' does not exist.")

            role.permissions.append(permission_obj)

        session.add(role)
        await session.commit()
        await session.refresh(role)

    return role


async def get_all_roles(db: AsyncSession):
    async with db as session:
        roles = await session.execute(select(Role))
        result = roles.scalars().all()
    if not roles:
        raise HTTPException(status_code=404, detail="No role found")
    return result

async def get_roles_with_permissions(db: AsyncSession):
    async with db as session:
        query = select(Role).options(joinedload(Role.users), joinedload(Role.permissions))
        roles = await session.execute(query)
        result = roles.all()
        import pdb; pdb.set_trace()
    if not result:
        raise HTTPException(status_code=404, detail="No role found")

    # Применяем unique() после all()
    result_unique = list(set(result))

    return result_unique

async def get_permission_by_name(permission_name: str, db: AsyncSession):
    permission = await db.execute(select(Permission).where(Permission.permission_type == permission_name))
    return permission.scalar()