import uuid

from serpent_web.data.sql.base_sql_model import BaseSqlModel as SerpentBaseSqlModel
from sqlalchemy import String
from sqlalchemy.orm import validates, class_mapper


# [str] designates the primary key type as string (in this case we use UUIDs but save them as strings)
class BaseSqlModel(SerpentBaseSqlModel[str]):
    __abstract__ = True  # abstract base class

    @classmethod
    def id_model_type(cls):
        return String

    @classmethod
    def default_id(cls):
        return lambda: str(uuid.uuid4())

    # validates that the primary key 'id' is a valid UUID4
    @validates("id")
    def validate_uuid(self, key, value):
        if value is None and key == 'id':
            return value
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except ValueError:
            raise ValueError(f"{key} must be a valid UUID4")
        if str(uuid_obj) != value:
            raise ValueError(f"{key} must be a valid UUID4")
        return value

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}
