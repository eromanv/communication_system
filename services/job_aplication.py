from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import JobApplication, JobApplicationAnswer

from schemas.schemas import JobApplicationSchemas


async def read_job_aplication_by_id(
    user_id: int, 
    db: AsyncSession, 
    sort_by, 
    filter_department: str, 
    filter_status: str 
):
    async with db as session:
        statement = select(JobApplication).filter_by(user_id=user_id).order_by(JobApplication.updated_at)
        
        # Добавление сортировки
        if sort_by:
            if sort_by == 'created_at':
                statement = statement.order_by(JobApplication.created_at)
            elif sort_by == 'updated_at':
                statement = statement.order_by(JobApplication.updated_at)
            elif sort_by == 'priority':
                statement = statement.order_by(JobApplication.priority)
        
        # Добавление фильтрации по отделу
        if filter_department:
            filter_department_list = [int(dep_id) for dep_id in filter_department.split(",")]
            statement = statement.filter(JobApplication.department_id.in_(filter_department_list))
        
        # Добавление фильтрации по статусу
        if filter_status:
            filter_status_list = [int(status_id) for status_id in filter_status.split(",")]
            statement = statement.filter(JobApplication.status_id.in_(filter_status_list))
            print(f'good choice for statuses: {filter_status_list}')
        
        

        result = await session.execute(statement)
        applications = result.scalars().all()
        
        if not applications:
            raise HTTPException(status_code=404, detail="Applications not found")
        
        return applications


async def read_own_job_applications(user_id: int, department_id: int, db: AsyncSession):
    """Прочитать заявки своего департамента. нужна роль"""
    async with db as session:
        statement = (
            select(JobApplication)
            .join(JobApplicationAnswer, JobApplicationAnswer.job_application_id == JobApplication.id)
            .filter(
                (JobApplication.user_id == user_id)
                & (JobApplicationAnswer.department_id == department_id)
            )
        )
        
        result = await session.execute(statement)
        job_applications = result.scalars().all()
        if not job_applications:
            raise HTTPException(status_code=404, detail="Applications not found")
        return job_applications



async def update_job_aplication(data: JobApplicationSchemas, id: int, db: AsyncSession):
    try:
        async with db as session:
            application = await session.get(JobApplication, id)
            if application:
                application.department_id = data.department_id
                application.status_id = data.status_id
                application.trouble_shooter_id = data.trouble_shooter_id
                application.title = data.title
                application.description = data.description
                application.priority = data.priority
                application.created_at = data.created_at.replace(tzinfo=None)
                application.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(application)
                return application
            else:
                raise HTTPException(status_code=404, detail="no application founded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"wrong update {str(e)}")


async def create_job_application(data: JobApplicationSchemas, db: AsyncSession):
    if not data.department_id:
        raise HTTPException(status_code=400, detail="Департамент не выбран")

    async with db as session:
        applicaton = JobApplication(
            department_id=data.department_id,
            status_id=3,
            trouble_shooter_id=data.trouble_shooter_id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            created_at=datetime.utcnow(),
            updated_at=None,
        )
        try:
            session.add(applicaton)
            await session.commit()
            await session.refresh(applicaton)
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Ошибка: {str(error)}")
    return applicaton    
    

async def delete_job_application(id: int, db: AsyncSession):
    async with db as session:
        statement = select(JobApplication).filter_by(id=id)
        result = await session.execute(statement)
        app = result.scalars().first()
        if not app:
            raise HTTPException(status_code=404, detail="Нет такой задачи")
        await session.delete(app)
        await session.commit()

        return {"message": "Application is deleted"}
