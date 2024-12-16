from serpent_web.domain.base_sql_manager import BaseSqlManager

from src.fastapi_reference.data.models.person import Person


class PersonManager(BaseSqlManager[Person]):
    pass
