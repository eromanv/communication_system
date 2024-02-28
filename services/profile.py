from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import PersonalInfo
from schemas.schemas import PersonalInfoSchemas, PersonalInfoUpdate
from services.roles import get_permission_by_name


async def read_profile_all(db: AsyncSession):
    async with db as session:
        statement = select(PersonalInfo)
        result = await session.execute(statement)
        profile = result.scalars().all()
    if not profile:
        raise HTTPException(status_code=404, detail="No users found")
    return profile


async def read_profile_id(user_id: int, db: AsyncSession):
    async with db as session:
        statement = select(PersonalInfo).filter_by(user_id=user_id)
        result = await session.execute(statement)
        profile = result.scalars().first()
    if profile is None:
        raise HTTPException(
            status_code=404, detail=f"profile with user id {user_id} is not founded"
        )
    return profile


async def change_profile(data: PersonalInfoSchemas, id: int, db: AsyncSession):
    """Изменить профиль пользователья на основе id."""
    try:
        async with db as session:
            profile = await session.get(PersonalInfo, id)
            if profile:
                profile.name = data.name
                profile.surname = data.surname
                profile.patronymic = data.patronymic
                profile.position_id = data.position_id
                profile.job_title_id = data.job_title_id
                profile.city = data.city
                await session.commit()
                await session.refresh(profile)
                return profile
            else:
                raise HTTPException(status_code=404, detail="No user found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wrong update: {str(e)}")
    
async def make_profile(data: PersonalInfoSchemas, db: AsyncSession):
    """Создать профиль с информацией."""
    try:
        # Проверка наличия права доступа для указанной роли
        role_id = data.role_id
        if role_id:
            permission_name = "create"  # Замените на нужное вам право доступа
            permission = await get_permission_by_name(permission_name, db)

            if not permission:
                raise HTTPException(
                    status_code=400,
                    detail=f"Role with id {role_id} does not have the required permission: {permission_name}",
                )

        # Остальной код остается без изменений
        profile = PersonalInfo(
            id=data.id,
            user_id=data.user_id,
            name=data.name,
            surname=data.surname,
            patronymic=data.patronymic,
            position_id=data.position_id,
            job_title_id=data.job_title_id,
            city=data.city,
            role_id=data.role_id,  # Указываем id роли пользователя
        )

        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    except HTTPException as error:
        raise error
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Something happened on the server with {str(e)}',
        )
    return profile
