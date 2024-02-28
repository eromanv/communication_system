from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import UserFeedback
from schemas.schemas import UserFeedbackSchemas

async def create_user_feedback(feedback: UserFeedbackSchemas, db: AsyncSession):
    db_feedback = UserFeedback(
        user_feedbacks_id = feedback.user_feedbacks_id,
        user_created_id = feedback.user_created_id,
        description = feedback.description,
        created_at = datetime.utcnow(),
    )
    try:
        db.add(db_feedback)
        await db.commit()
        await db.refresh(db_feedback)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f'something happend on a server with {str(error)}'
        )
    return db_feedback

async def read_feedback_all(db: AsyncSession):
    async with db as session:
        result = await session.execute(select(UserFeedback))
        feedback = result.scalars().all()
    if not feedback:
        raise HTTPException(status_code=404, detail="No feedback found")
    return feedback



