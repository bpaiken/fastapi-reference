from serpent_web.data.sql.base_sql_repository import BaseSqlRepository

from src.fastapi_reference.data.models.person import Person


class PersonRepository(BaseSqlRepository[Person]):
    pass
