import os
from dotenv import load_dotenv
from src.utils.db_conn import get_vector_store
from src.utils.embeddings import get_embeddings


load_dotenv()

def test_setup():
    print("--- DocuMend Diagnostic Start ---")
    
    try:
        # 1. Test Gemini Embeddings
        print("Testing Gemini Embeddings...")
        embed_model = get_embeddings()
        test_vector = embed_model.embed_query("Hello DocuMend")
        print(f"✅ Gemini Success! Vector size: {len(test_vector)}")

        # 2. Test Astra DB Connection
        print("\nConnecting to Astra DB...")
        vector_store = get_vector_store()
        
        # Check if we can reach the database
        # This will attempt to create the collection if it doesn't exist
        count = vector_store.add_texts(["Connection Test"])
        print(f"Astra DB Success! Test data indexed.")

    except Exception as e:
        print(f"\nError detected: {str(e)}")
        print("\nChecklist for fix:")
        print("- Is your GOOGLE_API_KEY correct?")
        print("- Is your ASTRA_DB_API_ENDPOINT starting with https://?")
        print("- Did you install requirements? (pip install langchain-google-genai langchain-astradb)")

if __name__ == "__main__":
    test_setup()