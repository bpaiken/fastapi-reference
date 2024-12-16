from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class BaseSchema(BaseModel):
    pass


class BaseSqlModelSchema(BaseSchema):
    id: str
    created_on: datetime
    updated_on: datetime

    @field_validator("id")
    @classmethod
    def check_uuid4(cls, value: str):
        if value is not None:
            try:
                uuid_value = UUID(value)
            except ValueError:
                raise ValueError("id must be a valid UUID string")

            if uuid_value.version != 4:
                raise ValueError("id must be a UUID version 4")

        return value

    @property
    def pk(self) -> str:
        return self.id

    # Pydantic v2
    model_config = {
        'from_attributes': True
    }

    # Pydantic v1
    # class Config:
    #     orm_mode = True
