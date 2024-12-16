from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from serpent_web.data.sql.sql_database_type import DatabaseType

load_dotenv()

class DatabaseSettings(BaseSettings):
    database_name: str
    database_url: str
    database_type: Optional[DatabaseType] = DatabaseType.POSTGRES


class _AppSettings(BaseSettings):
    database_settings: DatabaseSettings

    class Config:
        env_nested_delimiter = "__"
        extra = "ignore"