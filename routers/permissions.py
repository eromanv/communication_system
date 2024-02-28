from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from schemas.schemas import Permission as PermissionSchema
from services.permissions import get_all_permissions  
from sqlalchemy import select
from typing import List  

permission_router = APIRouter(tags=["permission"], prefix="/permissions")

@permission_router.get("/", response_model=List[PermissionSchema])  
async def read_all_permissions(db: AsyncSession = Depends(get_db)):
    permissions = await get_all_permissions(db)
    if not permissions:
        raise HTTPException(status_code=404, detail="Permissions not found")
    return permissions

