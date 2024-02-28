import os

from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# # Load the environment variables from the .env file
# load_dotenv()

# # Read the database connection settings from the environment variables
# DB_USERNAME = os.getenv("DB_USERNAME")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_DATABASE = os.getenv("DB_DATABASE")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")

# # Construct the database URL
# SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# # Create the engine and session maker
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create the base class
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@localhost:5432/my_db"

# engine = create_async_engine(settings.ASYNC_DATABASE_URL)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
