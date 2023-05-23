import sys
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, GPTListIndex
from llama_index.node_parser import SimpleNodeParser
from storage_context import get_storage_context

def get_metadata(file_path):
  return {
    "file_path": file_path.replace(sys.argv[1], '')
  }

print('loading documents')
documents = SimpleDirectoryReader(
  sys.argv[1],
  recursive=True, 
  exclude_hidden=True,
  file_metadata=get_metadata,
  exclude=[
    '**/tools/plcTester/public/**/*',
    '**/.git/**/*', 
    '**/node_modules/**/*', 
    "**/dist/**/*",
    "**/.yarn/**/*",
    "*.jpg", "*.png", "*.zip", "*.svg", "*.pdf", 
    "*.zip", "*.jpeg", "*.mp4", '*.deb', 
    '*.env', '*.ico', '*.job', '*.key', '*.mp3', 
    '*.pem', '*.rpm', '*.tff', '*.urp', 
    '*.webm', '*.woff2', '*.wrongextension', '*.gz', 
    '*.cab', '*.bmp', '*.dds', '*.ttf', '*.log',
  ],
).load_data()
print('finished loading documents')

print('loading nodes')
nodes = SimpleNodeParser().get_nodes_from_documents(documents)
print('finished loading nodes')

mongo_uri = "mongodb://127.0.0.1/db_docstore?replicaSet=eflex"

storage_context = get_storage_context()

print('saving documents to mongo')
storage_context.docstore.add_documents(nodes)
print('finished saving documents to mongo')

print('creating index')
GPTVectorStoreIndex(nodes, storage_context=storage_context)
GPTListIndex(nodes, storage_context=storage_context)
print('finished creating index')
