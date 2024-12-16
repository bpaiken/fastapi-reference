from contextvars import ContextVar

from fastapi import Depends
from sqlalchemy.orm import Session
from serpent_web.data.sql.sql_context import db_dependency

from src.fastapi_reference.data.repositories import TodoRepository, PersonRepository
from src.fastapi_reference.domain.managers import PersonManager, TodoManager
from src.fastapi_reference.host.handler import PersonHandler, TodoHandler
from src.fastapi_reference.settings import database_settings

# CONTEXT VARIABLES
session_context = ContextVar[Session]("session_context", default=None)


# Database contexts
def get_db_session() -> Session:
    session = session_context.get()
    if session is None:
        db_settings = database_settings
        dependency = db_dependency(
            database_url=db_settings.database_url,
            database_type=db_settings.database_type,
            database_name=db_settings.database_name,
        )

        session = next(dependency())

        session_context.set(session)

    return session


# Repositories
def get_person_repository(
        session: Session = Depends(get_db_session),
) -> PersonRepository:
    from src.fastapi_reference.data.repositories.person_repository import PersonRepository
    return PersonRepository(db=session)


def get_todo_repository(
        session: Session = Depends(get_db_session),
) -> TodoRepository:
    from src.fastapi_reference.data.repositories.todo_repository import TodoRepository
    return TodoRepository(db=session)


# Managers
def get_person_manager(
        repository: PersonRepository = Depends(get_person_repository),
) -> PersonManager:
    from src.fastapi_reference.domain.managers.person_manager import PersonManager
    return PersonManager(repository)


def get_todo_manager(
        repository: TodoRepository = Depends(get_todo_repository),
) -> TodoManager:
    from src.fastapi_reference.domain.managers.todo_manager import TodoManager
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
