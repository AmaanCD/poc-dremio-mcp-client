from typing import List

from pydantic import BaseModel

from models.columns_data import ColumnMetadata
from models.schema_meta_data import MetaData


class MetaDataDetails(BaseModel):
    schema_details : MetaData
    columnMetas : List[ColumnMetadata]
    description : str