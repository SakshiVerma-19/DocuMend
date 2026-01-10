import os
from langchain_astradb import AstraDBVectorStore
from src.utils.embeddings import get_embeddings
from dotenv import load_dotenv

load_dotenv()

def get_vector_store():
    return AstraDBVectorStore(
        embedding=get_embeddings(),
        collection_name="documend_collection",
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        namespace=os.getenv("ASTRA_DB_NAMESPACE"),
    )