import os
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_answer(question, context):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # The prompt forces Gemini to only use the provided text
    prompt = f"""
    You are a professional assistant for DocuMend. 
    Use the provided context to answer the question. 
    If the answer is NOT in the context, say "I don't have enough information in the document to answer that."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    response = llm.invoke(prompt)
    return response.content

def generate_summary(chunks):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3 
    )
    
    combined_text = "\n".join([doc.page_content for doc in chunks[:10]]) 
    
    prompt = f"""
    You are a professional research assistant. Provide a concise, one-page executive summary of the following text.
    Use the following structure:
    1. Key Objective: What is this document about?
    2. Main Findings/Points: Bulleted list of 5 key takeaways.
    3. Conclusion: Final summary sentence.
    
    Text:
    {combined_text}
    """
    
    response = llm.invoke(prompt)
    return response.content