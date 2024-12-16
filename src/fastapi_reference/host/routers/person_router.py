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
def get_people(
        skip: int = 0,
        limit: int = 100,
        search_text: str = None,
        handler: PersonHandler = Depends(get_person_handler),
) -> PaginatedGetPersonResponse:
    return handler.get_paginated(
        skip=skip,
        limit=limit,
        search_text=search_text,
    )


@person_router.get("/{person_id}")
def get_person(
        person_id: str,
        handler: PersonHandler = Depends(get_person_handler),
) -> GetPersonResponse:
    return handler.get_by_id(id=person_id)

@person_router.post("")
def create_person(
        schema: CreatePersonRequest,
        handler: PersonHandler = Depends(get_person_handler),
) -> GetPersonResponse:
    return handler.create(schema=schema)

@person_router.put("/{person_id}")
def update_todo(
        person_id: str,
        schema: CreatePersonRequest,
        handler: PersonHandler = Depends(get_person_handler),
)-> GetPersonResponse:
    return handler.update(id=person_id, schema=schema)


@person_router.delete("/{person_id}")
def delete_todo(
        person_id: str,
        handler: PersonHandler = Depends(get_person_handler),
) -> Response:
    handler.delete(id=person_id)
    return Response(status_code=204)