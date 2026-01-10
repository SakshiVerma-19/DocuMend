import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embeddings():
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("API Key not found. Ensure it is set in Streamlit Secrets.")
    
    return GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key 
    )