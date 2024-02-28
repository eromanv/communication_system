from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://Internet_Portal:Internet_Portal@0.0.0.0:5432/Internet_Portal_DB"
) #connect string for the database