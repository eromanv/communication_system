from functools import lru_cache

from config import Settings
from database import async_session

# Вызывается по время внедрения зависимости
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()

# Возврат существующего экземпляра DBSettings вместо создания нового
@lru_cache
def get_db_settings() -> Settings:
    return Settings()