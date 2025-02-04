import logging
from contextvars import ContextVar

from fastapi import Depends
from serpent_web.data.sql.sql_context import get_async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.fastapi_reference.data.repositories import TodoRepository, PersonRepository
from src.fastapi_reference.domain.managers import PersonManager, TodoManager
from src.fastapi_reference.host.handler import PersonHandler, TodoHandler
from src.fastapi_reference.settings import database_settings

_logger = logging.getLogger(__name__)

# CONTEXT VARIABLES
session_context = ContextVar[Session | AsyncSession]("session_context", default=None)


# Database contexts
async def get_db_session() -> AsyncSession:
    session = session_context.get()
    if session is None:
        db_settings = database_settings

        session_maker = get_async_session_maker(
            database_url=db_settings.database_url,
            database_type=db_settings.database_type,
            database_name=db_settings.database_name,
        )

        session = session_maker()
        session_context.set(session)

    async with session as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            _logger.exception(f"Async database session rollback due to exception: {e}")
            await session.rollback()
            raise


# Repositories
def get_person_repository(
        session: Session = Depends(get_db_session),
) -> PersonRepository:
    return PersonRepository(db=session)


def get_todo_repository(
        session: Session = Depends(get_db_session),
) -> TodoRepository:
    return TodoRepository(db=session)


# Managers
def get_person_manager(
        repository: PersonRepository = Depends(get_person_repository),
) -> PersonManager:
    return PersonManager(repository)


def get_todo_manager(
        repository: TodoRepository = Depends(get_todo_repository),
) -> TodoManager:
    return TodoManager(repository)


# Handlers
def get_person_handler(
        manager: PersonManager = Depends(get_person_manager),
) -> PersonHandler:
    return PersonHandler(manager)


def get_todo_handler(
        manager: TodoManager = Depends(get_todo_manager),
) -> TodoHandler:
    return TodoHandler(manager)

