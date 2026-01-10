import os
import streamlit as st  # Correct way to import Streamlit
from langchain_astradb import AstraDBVectorStore
from src.utils.embeddings import get_embeddings
from dotenv import load_dotenv

load_dotenv()

def get_vector_store():
    api_endpoint = st.secrets.get("ASTRA_DB_API_ENDPOINT") or os.getenv("ASTRA_DB_API_ENDPOINT")
    token = st.secrets.get("ASTRA_DB_APPLICATION_TOKEN") or os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    namespace = st.secrets.get("ASTRA_DB_NAMESPACE") or os.getenv("ASTRA_DB_NAMESPACE")

    return AstraDBVectorStore(
        embedding=get_embeddings(),
        collection_name="documend_collection",
        api_endpoint=api_endpoint,
        token=token,
        namespace=namespace,
    )