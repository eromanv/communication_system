from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas.schemas import PersonalInfoSchemas, PersonalInfoUpdate
from services.profile import change_profile, make_profile, read_profile_all, read_profile_id

profile = APIRouter(prefix="/users", tags=["profile_info"])


@profile.get("/personal_info/")
async def get_profile(db: AsyncSession = Depends(get_db)):
    profile = await read_profile_all(db)
    return profile


@profile.get("/{user_id}/personal_info/")
async def get_profile_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        profile = await read_profile_id(user_id, db)
        return profile
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"detail": error.detail}
        )

@profile.post('/personal_info/')
async def create_personal_info_profile(data: PersonalInfoSchemas, db: AsyncSession = Depends(get_db)):
    try:
        profile = await make_profile(data, db)
        return profile
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@profile.patch("/{user_id}/personal_info/")
async def make_change_profile(
    data: PersonalInfoSchemas, user_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        profile = await change_profile(data, user_id, db)
        return profile
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
