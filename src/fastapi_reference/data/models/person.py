from src.fastapi_reference.data.models.base_sql_model import BaseSqlModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Person(BaseSqlModel):
    name = Column(String, nullable=False)

    # relationships
    todos = relationship("Todo", back_populates="person", lazy="joined")  # not lazily loaded

