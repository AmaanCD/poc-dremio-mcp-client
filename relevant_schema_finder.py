from models.schema_data import TableMetadata


def get_relevant_schema_finder(result):
    data : list[TableMetadata]= []
    for document in result:
        data.append(TableMetadata(**document))

    return data

