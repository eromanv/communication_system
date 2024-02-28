from pydantic_settings import BaseSettings

# class DBSettings(BaseSettings):
#     username: str
#     password: str
#     database: str
#     host: str
#     port: str
#
#     class Config:
#         env_prefix = "DB_"
#         env_file = ".env"

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()