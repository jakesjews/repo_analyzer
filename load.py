import nest_asyncio
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.storage_context import StorageContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.index_store import MongoIndexStore
from llama_index.vector_stores import RedisVectorStore

nest_asyncio.apply()

print('loading documents')

documents = SimpleDirectoryReader(
  '/Users/jacob/dev/eflexsystems/eflex', 
  recursive=True, 
  exclude_hidden=True,
  exclude=[
    "*.jpg", "*.png", "*.zip", "*.svg", "*.pdf", "*.zip", "*.jpeg", "*.mp4", '*.deb', 
    '*.env', '*.ico', '*.job', '*.key', '*.mp3', '*.pem', '*.rpm', '*.tff', '*.urp', 
    '*.webm', '*.woff2', '*.wrongextension', '*.gz', '*.cab'
  ],
).load_data()

print('finished loading documents')

parser = SimpleNodeParser()
print('loading nodes')
nodes = parser.get_nodes_from_documents(documents)
print('finished loading nodes')

mongo_uri = "mongodb://127.0.0.1/db_docstore?replicaSet=eflex"

print('saving documents to mongo')
docstore = MongoDocumentStore.from_uri(uri=mongo_uri)
docstore.add_documents(nodes)
print('finished saving documents to mongo')

index_store = MongoIndexStore.from_uri(mongo_uri)

vector_store = RedisVectorStore(
  index_name="eflex",
  index_prefix="llama",
  redis_url="redis://localhost:6379",
)

storage_context = StorageContext.from_defaults(
  docstore=docstore,
  index_store=index_store,
  vector_store=vector_store
)

print('creating index')
index = GPTVectorStoreIndex(nodes, storage_context=storage_context)
print('finished creating index')

docstore.persist(persist_path="")
index_store.persist(persist_path="")
vector_store.persist(persist_path="")
