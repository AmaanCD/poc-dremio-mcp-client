from typing import List

from models.meta_data_details import MetaDataDetails
from operations.vector_db_formator import format_for_vector_db
from client.vector_store_client import get_vector_store
from operations.meta_data_creator import create_meta_data


async def ingest():
    vector_store = get_vector_store()
    count = vector_store._collection.count()
    if count == 0:
        print(count)
        meta_data = await create_meta_data()
        documents = [format_for_vector_db(data) for data in meta_data]
        vector_store.add_documents(documents)