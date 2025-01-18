from datetime import datetime

from pydantic import BaseModel, field_serializer, field_validator


class Token(BaseModel):
    id: int
    role: int

    @field_serializer('id', 'role')
    @staticmethod
    def serialize(value):
        return str(value)

    @field_validator('id', 'role')
    @staticmethod
    def validate(value):
        return int(value)



