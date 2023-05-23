import sys
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.storage_context import StorageContext
from llama_index.storage.index_store import MongoIndexStore
from llama_index.vector_stores import RedisVectorStore
from llama_index import load_index_from_storage

mongo_uri = "mongodb://127.0.0.1/db_docstore?replicaSet=eflex"

storage_context = StorageContext.from_defaults(
  docstore=MongoDocumentStore.from_uri(uri=mongo_uri),
  index_store=MongoIndexStore.from_uri(uri=mongo_uri),
  vector_store=RedisVectorStore(
    index_name="eflex",
    index_prefix="llama",
    redis_url="redis://localhost:6379",
  )
)

index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query(sys.argv[1])
print(response)
