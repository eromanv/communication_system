from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import JobApplicationAnswer

from schemas.schemas import JobApplicationSchemas

async def read_job_applcation_answers_by_foreing_id(id: int, db: AsyncSession):
    '''Возможность просмотреть ответ по заявке.'''
    async with db as session:
        statement = JobApplicationAnswer.filter_by(job_application_id=id)
        result = await session.execute(statement)
        answer = result.scalars.all()
        if answer is None:
            raise HTTPException(status_code=404, detail='No answer is found')
        return answer


async def check_status_of_application(id: int, db: AsyncSession)
    """Возможность просмотреть статус заявки."""
    async with db as session:
        statement = select(JobApplicationAnswer.status_id).filter_by(job_application_id=id)
        result = await session.execute(statement)
        status_id = result.scalar()
        if status_id is None:
            raise HTTPException(status_code=404, detail='No answer is found')
        return {'status_id': status_id}

async def sort_answers_by_created_time():
    """Возможность сортировки заявок по дате создания."""
    pass

async def sort_answers_by_updated_time():
    """Возможность сортировки заявок по дате обновления."""
    pass


Возможность выбрать отдел для отправки заявки 
Возможность добавить заголовок заявки
Возможность добавить описание заявки
Возможность добавить файлы к заявке
Возможность добавить приоритет к заявке:От 1 до 10



Возможность сортировки заявок по дате создания

Возможность сортировки заявок по приоритету
Возможность фильтрации заявок по отделу
Возможность фильтрации заявок по статусу
Завершенные заявки отображаются только при выборе соответствующего фильтра статуса
Возможность просмотреть личный кабинет исполнителя заявки
Возможность добавить ответ на свою заявку
Просмотреть всю историю добавления ответов на заявку