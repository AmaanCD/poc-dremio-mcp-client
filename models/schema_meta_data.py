from pydantic import Field, BaseModel


class MetaData(BaseModel):
    table_catalog : str = Field(alias="TABLE_CATALOG")
    table_schema : str = Field(alias="TABLE_SCHEMA")
    table_name : str = Field(alias="TABLE_NAME")
    table_type : str = Field(alias="TABLE_TYPE")

