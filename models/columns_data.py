from pydantic import BaseModel, Field

from models.type_info import TypeInfo


class ColumnMetadata(BaseModel):
    name: str
    type_info: TypeInfo = Field(alias="type")