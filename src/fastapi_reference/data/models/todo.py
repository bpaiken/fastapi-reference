from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.types import TIMESTAMP
from serpent_web.core.util.datetime_helpers import utc_now_time_aware
from sqlalchemy.orm import relationship

from src.fastapi_reference.data.models.base_sql_model import BaseSqlModel


class Todo(BaseSqlModel):
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(TIMESTAMP(timezone=True), nullable=True)
    completed = Column(String, nullable=False, default="false")

    # relationships
    person_id = Column(String, ForeignKey('person.id'), nullable=False)
    person = relationship("Person", back_populates="todos")
