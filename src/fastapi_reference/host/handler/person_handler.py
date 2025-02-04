from src.fastapi_reference.data.models.person import Person
from src.fastapi_reference.host.handler.base_sql_model_handler import BaseSqlModelHandler


class PersonHandler(BaseSqlModelHandler[Person]):
    pass