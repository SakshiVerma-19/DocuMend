from src.utils.db_conn import get_vector_store

def get_relevant_context(question):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(question, k=3)
    

    context = "\n---\n".join([doc.page_content for doc in results])
    return context

def get_relevant_context_with_sources(question):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(question, k=3)
    
    context_list = []
    sources = []
    
    for doc in results:
        page = doc.metadata.get("page", "Unknown")
        source_text = f"[Page {page}]: {doc.page_content}"
        context_list.append(source_text)
        sources.append(f"Page {page}")
        
    context = "\n---\n".join(context_list)
    return context, list(set(sources))