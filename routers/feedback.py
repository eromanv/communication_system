from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from schemas.schemas import UserFeedbackSchemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Request
from dependencies import get_db
from services.feedback import create_user_feedback, read_feedback_all
import asyncio

feedback = APIRouter(prefix='/feedback', tags=['feedback'])
# templates = Jinja2Templates(directory="templates")


"""
Здесь путь, который выдаёт записи пользователя по его ID (чтобы отправитель смог посмотреть свои)
"""

"""
Здесь путь, который выдает все записи (но он должен быть ограничен по правам доступа)
"""
@feedback.get('/')
async def get_feedback_all(db: AsyncSession = Depends(get_db)):
    feedback = await read_feedback_all(db)
    return feedback

"""
Здесь пробный GET для тестовой странички
"""
# @feedback.get('/')
# async def get_feedback_all(request: Request, db: AsyncSession = Depends(get_db)):
#     feedback_entries = await read_feedback_all(db)
#     return templates.TemplateResponse("feedback.html", {"request": request, "feedback": feedback_entries})
"""
Здесь путь, который позволяет отправить запись на эту страницу
"""
@feedback.post('/')
async def post_feedback(data: UserFeedbackSchemas, db: AsyncSession = Depends(get_db)):
    try:
        feedback = await create_user_feedback(data, db)
        return feedback
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    

