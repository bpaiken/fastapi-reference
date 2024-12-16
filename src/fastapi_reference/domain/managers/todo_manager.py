from serpent_web.domain.base_sql_manager import BaseSqlManager

from src.fastapi_reference.data.models.todo import Todo


class TodoManager(BaseSqlManager[Todo]):
    pass