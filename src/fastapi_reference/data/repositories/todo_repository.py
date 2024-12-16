from serpent_web.data.sql.base_sql_repository import BaseSqlRepository

from src.fastapi_reference.data.models.todo import Todo


class TodoRepository(BaseSqlRepository[Todo]):
    pass
