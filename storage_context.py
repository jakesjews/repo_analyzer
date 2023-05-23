from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.storage_context import StorageContext
from llama_index.storage.index_store import MongoIndexStore
from llama_index.vector_stores import RedisVectorStore

mongo_uri = "mongodb://127.0.0.1/db_docstore?replicaSet=eflex"
redis_url = "redis://localhost:6379"

def get_storage_context():
  return StorageContext.from_defaults(
    docstore=MongoDocumentStore.from_uri(uri=mongo_uri),
    index_store=MongoIndexStore.from_uri(uri=mongo_uri),
    vector_store=RedisVectorStore(
      index_name="eflex",
      index_prefix="llama",
      redis_url=redis_url,
    )
  )
