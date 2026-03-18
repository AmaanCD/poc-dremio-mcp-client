import json
from typing import List

from models.columns_data import ColumnMetadata
from models.meta_data_details import MetaDataDetails
from models.schema_meta_data import MetaData
from components.dremio_tools import get_tools


_docs : List[MetaData] = []
_parent_query = """
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA."TABLES"
WHERE TABLE_TYPE != 'SYSTEM_TABLE' and TABLE_TYPE != 'TABLE'
"""
async def create_meta_data():
    global _docs

    if _docs:
        return _docs

    tools = await get_tools()

    by_name = {t.name: t for t in tools}
    parent_result = await by_name["RunSqlQuery"].ainvoke({
        "query": _parent_query
    })

    query_parent = next( record for record in parent_result if record["type"] == "text")
    data = json.loads(query_parent["text"])["result"]
    final_meta_data_list : List[MetaDataDetails] = []
    #print(data)
    for item in data:
        current_document = MetaData.model_validate(item)
        print(f"{current_document.table_schema}.{current_document.table_name}")
        schema = await by_name["GetSchemaOfTable"].ainvoke({
            "table_name" : f"{current_document.table_schema}.{current_document.table_name}"
        })

        _docs.append(current_document)
        print(schema)
        column_meta = []
        description_wiki : str | None = None
        for sc in schema:
            #print(sc["text"])
            schema_data=sc["text"]
            schema_data = json.loads(schema_data)
            column_meta = [ ColumnMetadata.model_validate( col) for col in schema_data["fields"]]
            description_wiki = schema_data["description"]
            #print(column_meta)

        final_meta_data = MetaDataDetails(
            schema_details=current_document,
            columnMetas=column_meta,
            description=description_wiki
        )
        print(final_meta_data)
        final_meta_data_list.append(final_meta_data)



    return final_meta_data_list












