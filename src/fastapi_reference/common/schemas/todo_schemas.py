from datetime import datetime
from typing import Optional

from serpent_web.data.data_schemas import PaginatedList

from src.fastapi_reference.common.schemas.base_schema import BaseSchema, BaseSqlModelSchema


class BaseTodoSchema(BaseSchema):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    due_date: Optional[datetime] = None
    person_id: str


class CreateTodoRequest(BaseTodoSchema):
    pass


class UpdateTodoRequest(BaseTodoSchema):
    pass


class GetTodoResponse(BaseSqlModelSchema, BaseTodoSchema):
    completed: bool  # not optional


class PaginatedGetTodoResponse(PaginatedList[GetTodoResponse]):
    pass
