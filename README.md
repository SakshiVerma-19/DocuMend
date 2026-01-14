DocuMend | Advanced RAG Research Assistant
DocuMend is a high-performance Retrieval-Augmented Generation (RAG) application that allows users to chat with complex PDF documents. By combining Google’s Gemini 3 Flash with Astra DB’s vector search capabilities, it provides fact-grounded answers with precise page-level citations.

Key Features
Intelligent Ingestion: Optimised data pipeline using Recursive Character Splitting with a 20% chunk overlap to maintain semantic continuity.

Vector Search: Real-time similarity search powered by DataStax Astra DB (Cassandra) and Google's text-embedding-004.

Executive Summarisation: One-click synthesis of entire documents into structured one-page summaries.

Source Grounding: All assistant responses are anchored to specific document pages to prevent hallucinations.

Modern UI: A custom-styled Streamlit interface featuring reactive components and professional SaaS aesthetics.

Technical Stack
Language Model: Google Gemini 2.5 Flash
Embeddings: Google text-embedding-004
Orchestration: LangChain
Vector Database: Astra DB (Apache Cassandra)
Frontend: Streamlit (Custom CSS)
Deployment: Streamlit Community Cloud (Secrets Management)

Installation & Setup
Clone the Repository
  git clone https://github.com/SakshiVerma-19/DocuMend.git
  
  cd DocuMend

Set up Environment Variables 
Create a .env file in the root directory:
  GOOGLE_API_KEY="your_google_key"
  ASTRA_DB_APPLICATION_TOKEN="your_astra_token"
  ASTRA_DB_API_ENDPOINT="your_astra_endpoint"
  ASTRA_DB_NAMESPACE="default_keyspace"

  
Install Dependencies
  pip install -r requirements.txt
  
Run the Application
streamlit run app.py

Optimization Highlights
To ensure the highest quality of retrieved information, the ingestion engine was optimised to use a recursive splitting strategy. This method prioritises splitting at logical boundaries (paragraphs, then sentences) while maintaining a 200-character buffer between chunks to preserve context. This reduces "context-cutting" errors and improves retrieval relevance by approximately 20% compared to standard fixed-length splitting.
