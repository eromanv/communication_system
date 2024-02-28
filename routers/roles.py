from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from schemas.schemas import RoleSchemas
from services.roles import create_role, get_all_roles, get_roles_with_permissions

role_router = APIRouter(tags=["role"], prefix="/roles")

@role_router.get("/")
async def get_roles(db: AsyncSession = Depends(get_db)):
    roles = await get_all_roles(db)
    return roles

@role_router.post('/')
async def post_roles_into(role_data: RoleSchemas, permissions: List[str], db: AsyncSession = Depends(get_db)):
    role = await create_role(role_data, permissions, db)
    return role

@role_router.get("/perm/")
async def get_roles_with_perm(db: AsyncSession = Depends(get_db)):
    roles_ext = await get_roles_with_permissions(db)
    return roles_ext
