from src.fastapi_reference.data.models.person import Person
from src.fastapi_reference.data.models.todo import Todo

# We add model references here so they can be picked by alembic for 'code first' migrations
__all__ = [
    "Todo",
    "Person",
]

