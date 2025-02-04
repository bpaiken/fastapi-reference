import logging
from typing import TypeVar, Type, get_args, Generic

from fastapi import HTTPException
from serpent_web.data.data_schemas import PaginatedList
from serpent_web.domain.base_sql_manager import BaseSqlManager

from src.fastapi_reference.common.schemas.base_schema import BaseSchema
from src.fastapi_reference.data.models.base_sql_model import BaseSqlModel

_logger = logging.getLogger(__name__)
TModel = TypeVar('TModel', bound=BaseSqlModel)


class BaseSqlModelHandler(Generic[TModel]):
    """
        Generic Base handler with passthrough CRUD operations
        Note: these methods are able to return the db model directly to the router due to FastAPI/Pydantic integration with SQLAlchemy.
        If the db model can not be directly mapped to the Pydantic schema response indicated in the router, the handler method will need to be overridden to return a schema.
    """

    def __init__(self, manager: BaseSqlManager[TModel]):
        self._manager = manager

    @classmethod
    def get_model_type(cls) -> Type[BaseSqlModel]:
        """
        Get the model type for the handler
        :return:
        """
        bases = cls.__orig_bases__
        return get_args(bases[0])[0]

    def get(self, query_filter: dict[str, any] = None, skip: int = 0, limit: int = 100) -> list[TModel]:
        """
        Get a list of models from the database
        :param limit: the number of records to return
        :param skip: the number of records to skip
        :param query_filter:
        :return:
        """

        result = self._manager.get(query_filter=query_filter, skip=skip, limit=limit)
        return result

    async def get_async(self, query_filter: dict[str, any] = None, skip: int = 0, limit: int = 100) -> list[TModel]:
        """
        Get a list of models from the database
        :param limit: the number of records to return
        :param skip: the number of records to skip
        :param query_filter:
        :return:
        """

        result = await self._manager.get_async(query_filter=query_filter, skip=skip, limit=limit)
        return result

    def get_by_id(self, id: str) -> TModel:
        """
        Retrieve a single object as specified by its primary key.
        :param id: The model's primary key (e.g., 'id')
        :return: The model
        """
        return self._manager.get_by_id(id)

    async def get_by_id_async(self, id: str) -> TModel:
        """
        Retrieve a single object as specified by its primary key.
        :param id: The model's primary key (e.g., 'id')
        :return: The model
        """
        return await self._manager.get_by_id_async(id)

    def get_paginated(
            self,
            query_filter: dict[str, any] = None,
            skip: int = 0,
            limit: int = 100,
            order_by: list[str] = None,
            search_text: str = None
    ) -> PaginatedList[TModel]:
        """
        Get a list of models from the database
        :param limit: the number of records to return
        :param skip: the number of records to skip
        :param query_filter: dictionary of key-value pairs for filtering the query
        :param order_by: list of fields to order by
        :param search_text: text to search for
        :return:
        """

        return self._manager.get_paginated(
            query_filter=query_filter,
            skip=skip,
            limit=limit,
            order_by=order_by,
            search_text=search_text
        )

    async def get_paginated_async(
            self,
            query_filter: dict[str, any] = None,
            skip: int = 0,
            limit: int = 100,
            order_by: list[str] = None,
            search_text: str = None
    ) -> PaginatedList[TModel]:
        """
        Get a list of models from the database
        :param limit: the number of records to return
        :param skip: the number of records to skip
        :param query_filter: dictionary of key-value pairs for filtering the query
        :param order_by: list of fields to order by
        :param search_text: text to search for
        :return:
        """

        return await self._manager.get_paginated_async(
            query_filter=query_filter,
            skip=skip,
            limit=limit,
            order_by=order_by,
            search_text=search_text
        )

    def create(self, schema: BaseSchema, defer_commit=False) -> TModel:
        """
        Create a model in the database
        :param schema:
        :param defer_commit: optional defer commit
        :return:
        """
        model_type = self.get_model_type()
        model = model_type(**schema.model_dump())

        return self._manager.create(model, defer_commit)

    async def create_async(self, schema: BaseSchema, defer_commit=False) -> TModel:
        """
        Create a model in the database
        :param schema:
        :param defer_commit: optional defer commit
        :return:
        """
        model_type = self.get_model_type()
        model = model_type(**schema.model_dump())

        return await self._manager.create_async(model, defer_commit)

    def update(self, id: str, schema: BaseSchema, defer_commit=False) -> TModel:
        """
        Update a model in the database
        :param id: The model's primary key (e.g., 'id')
        :param schema:
        :param defer_commit: optional defer commit
        :return:
        """
        model_dict = schema.model_dump(exclude_unset=True)
        model = self.get_by_id(id)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model with id {schema.id} not found")

        for key, value in model_dict.items():
            setattr(model, key, value)

        return self._manager.update(model, defer_commit)

    async def update_async(self, id: str, schema: BaseSchema, defer_commit=False) -> TModel:
        """
        Update a model in the database
        :param id: The model's primary key (e.g., 'id')
        :param schema:
        :param defer_commit: optional defer commit
        :return:
        """
        model_dict = schema.model_dump(exclude_unset=True)
        model = await self.get_by_id_async(id)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model with id {schema.id} not found")

        for key, value in model_dict.items():
            setattr(model, key, value)

        return await self._manager.update_async(model, defer_commit)

    def delete(self, id: str, defer_commit=False) -> None:
        """
        Delete a model in the database
        :param id: The model's primary key (e.g., 'id')
        :param defer_commit: optional defer commit
        :return:
        """
        model = self.get_by_id(id)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model with id {id} not found")

        self._manager.delete(id, defer_commit)

    async def delete_async(self, id: str, defer_commit=False) -> None:
        """
        Delete a model in the database
        :param id: The model's primary key (e.g., 'id')
        :param defer_commit: optional defer commit
        :return:
        """
        model = await self.get_by_id_async(id)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model with id {id} not found")

        await self._manager.delete_async(id, defer_commit)