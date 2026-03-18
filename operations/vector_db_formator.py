from langchain_core.documents import Document


def format_for_vector_db(data) :

        full_name = f"Table Name : {data.schema_details.table_schema}.{data.schema_details.table_name}"
        print(full_name)
        columns = []
        for col in data.columnMetas:
            columns.append(f"-  {col.name} {col.type_info.name}")
        column_block= ", ".join(columns)

        content = f"""
            {full_name}
            description : {data.description}
            columns : {column_block} 
            
    """

        vector_meta_data = {
                "table_schema" : data.schema_details.table_schema,
                "table_name" : data.schema_details.table_name,
                "full_table_name" : full_name,
                "columns" : ", ".join(col.name for col in data.columnMetas ),
                "column_type" : ", ".join(col.type_info.name for col in data.columnMetas)

            }
        return Document(page_content=content,meta_data=vector_meta_data)





