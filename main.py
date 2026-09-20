import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from dotenv import load_dotenv
from src.ingestion.parser import process_pdf
from src.utils.db_conn import get_vector_store
from src.inference.retriever import get_relevant_context
from src.inference.generator import generate_answer

load_dotenv()

def main():
    print("DocuMend: Professional RAG System")
    
    # 1. Ask to ingest a new PDF
    choice = input("Do you want to upload a new PDF? (y/n): ").lower()
    if choice == 'y':
        pdf_name = input("Enter the PDF filename in the /data folder (e.g., sample.pdf): ")
        pdf_path = f"data/{pdf_name}"
        
        if os.path.exists(pdf_path):
            print("Extracting text and creating embeddings...")
            chunks = process_pdf(pdf_path)
            vector_store = get_vector_store()
            vector_store.add_documents(chunks)
            print("Document successfully indexed!")
        else:
            print(f"Error: {pdf_path} not found.")

    # 2. Start Chatting
    print("\n💬 You can now chat with your documents! (Type 'exit' to quit)")
    while True:
        query = input("\nQuestion: ")
        if query.lower() == 'exit': break
        
        print("🔍 Searching and Thinking...")
        context = get_relevant_context(query)
        answer = generate_answer(query, context)
        
        print(f"\nDocuMend: {answer}")

if __name__ == "__main__":
    main()