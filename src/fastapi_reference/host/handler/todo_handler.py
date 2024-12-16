from src.fastapi_reference.data.models.todo import Todo
from src.fastapi_reference.host.handler.base_sql_model_handler import BaseSqlModelHandler


class TodoHandler(BaseSqlModelHandler[Todo]):
    pass
