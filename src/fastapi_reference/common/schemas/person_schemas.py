from serpent_web.data.data_schemas import PaginatedList

from src.fastapi_reference.common.schemas.base_schema import BaseSchema, BaseSqlModelSchema
from src.fastapi_reference.common.schemas.todo_schemas import GetTodoResponse


class BasePersonSchema(BaseSchema):
    name: str


class CreatePersonRequest(BasePersonSchema):
    pass


class UpdatePersonRequest(BasePersonSchema):
    pass


class GetPersonResponse(BaseSqlModelSchema, BasePersonSchema):
    id: str
    todos: list[GetTodoResponse]

    # pass

class GetManyPersonResponse(BasePersonSchema):
    id: str


class PaginatedGetPersonResponse(PaginatedList[GetManyPersonResponse]):
    pass