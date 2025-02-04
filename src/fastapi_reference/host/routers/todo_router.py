from fastapi import APIRouter, Depends, Response

from src.fastapi_reference.common.schemas.todo_schemas import PaginatedGetTodoResponse, GetTodoResponse, \
    CreateTodoRequest
from src.fastapi_reference.dependencies import get_todo_handler
from src.fastapi_reference.host.handler import TodoHandler

todo_router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@todo_router.get("")
async def get_todos(
        skip: int = 0,
        limit: int = 100,
        search_text: str = None,
        handler: TodoHandler = Depends(get_todo_handler),
) -> PaginatedGetTodoResponse:
    return await handler.get_paginated_async(
        skip=skip,
        limit=limit,
        search_text=search_text,
    )


@todo_router.get("/{todo_id}")
async def get_todo(
        todo_id: str,
        handler: TodoHandler = Depends(get_todo_handler),
) -> GetTodoResponse:
    return await handler.get_by_id_async(id=todo_id)


@todo_router.post("")
async def create_todo(
        schema: CreateTodoRequest,
        handler: TodoHandler = Depends(get_todo_handler),
) -> GetTodoResponse:
    return await handler.create_async(schema=schema)


@todo_router.put("/{todo_id}")
async def update_todo(
        todo_id: str,
        schema: CreateTodoRequest,
        handler: TodoHandler = Depends(get_todo_handler),
) -> GetTodoResponse:
    return await handler.update_async(id=todo_id, schema=schema)


@todo_router.delete("/{todo_id}")
async def delete_todo(
        todo_id: str,
        handler: TodoHandler = Depends(get_todo_handler),
) -> Response:
    await handler.delete_async(id=todo_id)
    return Response(status_code=204)
