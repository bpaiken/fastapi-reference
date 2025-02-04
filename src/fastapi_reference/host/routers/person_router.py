from fastapi import APIRouter, Depends, Response

from src.fastapi_reference.common.schemas.person_schemas import PaginatedGetPersonResponse, GetPersonResponse, \
    CreatePersonRequest
from src.fastapi_reference.dependencies import get_person_handler
from src.fastapi_reference.host.handler import PersonHandler

person_router = APIRouter(
    prefix="/people",
    tags=["people"],
)


@person_router.get("")
async def get_people(
        skip: int = 0,
        limit: int = 100,
        search_text: str = None,
        handler: PersonHandler = Depends(get_person_handler)
) -> PaginatedGetPersonResponse:
    return await handler.get_paginated_async(
        skip=skip,
        limit=limit,
        search_text=search_text,
    )

@person_router.get("/{person_id}")
async def get_person(
        person_id: str,
        handler: PersonHandler = Depends(get_person_handler),
) -> GetPersonResponse:
    return await handler.get_by_id_async(id=person_id)

@person_router.post("")
async def create_person(
        schema: CreatePersonRequest,
        handler: PersonHandler = Depends(get_person_handler),
) -> GetPersonResponse:
    return await handler.create_async(schema=schema, defer_commit=True)

@person_router.put("/{person_id}")
async def update_todo(
        person_id: str,
        schema: CreatePersonRequest,
        handler: PersonHandler = Depends(get_person_handler),
)-> GetPersonResponse:
    return await handler.update_async(id=person_id, schema=schema)


@person_router.delete("/{person_id}")
async def delete_todo(
        person_id: str,
        handler: PersonHandler = Depends(get_person_handler),
) -> Response:
    await handler.delete_async(id=person_id)
    return Response(status_code=204)