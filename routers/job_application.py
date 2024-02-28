from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas.schemas import JobApplicationSchemas
from services.job_aplication import create_job_application, delete_job_application, read_job_aplication_by_id, read_own_job_applications, update_job_aplication

job_application_router = APIRouter(prefix='/applications')

@job_application_router.get("/{user_id}/")
async def get_app_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    sort_by: str = Query(None, description="Sort applications by 'created_at', 'updated_at', or 'priority'"),
    filter_department: str = Query(None, description="Filter applications by department"),
    filter_status: str = Query(None, description="Filter applications by status"),
):
    try:
        app = await read_job_aplication_by_id(user_id, db, sort_by=sort_by, filter_department=filter_department, filter_status=filter_status)
        return app
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"detail": error.detail}
        )
@job_application_router.post('/')
async def post_app(data:JobApplicationSchemas, db: AsyncSession = Depends(get_db)):
    try:
        app = await create_job_application(data, db)
        return app
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={'detail': e.detail})
    
@job_application_router.get('/')
async def get_own_applications(user_id: int, department_id: int, db: AsyncSession = Depends(get_db)):
    try:
        app = await read_own_job_applications(user_id, department_id, db)
        return app
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={'detail': e.detail})

@job_application_router.patch('/{id}/')
async def change_app(data: JobApplicationSchemas, id: int, db: AsyncSession = Depends(get_db)):
    try:
        app = await update_job_aplication(data, id, db)
        return app
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={'detail': e.detail})
    
@job_application_router.delete("/{id}")
async def delete_app(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_job_application(id, db)