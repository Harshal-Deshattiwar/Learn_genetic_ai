from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

load_dotenv()
pdf_path = Path(__file__).parent / "notes.pdf"

# load file in python program
loader = PyPDFLoader(file_path=pdf_path)

docs = loader.load()

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)

chunks = text_splitter.split_documents(documents = docs)


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding= embedding_model,
    url= "http://localhost:6333",
    collection_name = "learning_rag"
)

print("indexing of document done")