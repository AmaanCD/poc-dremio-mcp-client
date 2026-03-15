from pydantic import BaseModel



class Columns(BaseModel):
    name : str
    type : str


class TableMetadata(BaseModel):
    fqn : str
    table_type : str
    score : float
    description : str
    columns : list[Columns]
    schema : str
    table : str
