import sys
from llama_index import load_index_from_storage
from storage_context import get_storage_context

storage_context = get_storage_context()
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query(sys.argv[1])
print(response)
