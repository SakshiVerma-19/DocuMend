import streamlit as st
import os
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(page_title="DocuMend AI", page_icon="📄", layout="wide")

# 2. Custom Professional Styling
st.markdown("""
   <style>
    .main { background-color: #fcfcfc; }
    
    /* Light Blue Instruction Box with Opacity */
    .instruction-box {
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #007bff;
        background-color: rgba(0, 123, 255, 0.1); /* Light blue with 10% opacity */
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 2rem;
        color: #40E0D0;
    }

    /* Button Styling Logic */
    /* Generate Summary - Green */
    div.stButton > button:first-child[data-testid="stBaseButton-secondary"] {
        border-color: #28a745;
        color: #28a745;
    }
    div.stButton > button:hover {
        background-color: rgba(40, 167, 69, 0.1);
        border-color: #218838;
    }

    /* Reset & Clear - Red (Targeting specific keys or positions) */
    /* We will use a more direct approach by wrapping them in markdown containers below */
    .red-button button {
        border-color: #FF0000 !important;
        color: #FF0000 !important;
    }
    .red-button button:hover {
        background-color: rgba(255, 0, 0, 0.1) !important;
        color: #cc0000 !important;
    }

    .green-button button {
        border-color: #28a745 !important;
        color: #28a745 !important;
    }
    .green-button button:hover {
        background-color: rgba(40, 167, 69, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Session State (Order is critical!)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chunks" not in st.session_state:
    st.session_state.current_chunks = None
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

# Logic to hide welcome box once chat starts
if len(st.session_state.messages) > 0:
    st.session_state.show_welcome = False

# 4. Imports & Logic
load_dotenv()
from src.ingestion.parser import process_pdf
from src.utils.db_conn import get_vector_store
from src.inference.retriever import get_relevant_context_with_sources
from src.inference.generator import generate_answer, generate_summary

st.title("DocuMend")

# 5. Welcome Hero Section
if st.session_state.show_welcome:
    st.markdown("""
    <div class="instruction-box">
        <h4 style="margin-top:0; color: #40E0D0;">System Overview</h4>
        <p>DocuMend uses Retrieval-Augmented Generation to analyze documents without hallucinations.</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div><strong>1. Setup</strong><br><small>Upload a PDF and click Index.</small></div>
            <div><strong>2. Process</strong><br><small>Text is converted to vectors in Astra DB.</small></div>
            <div><strong>3. Analyze</strong><br><small>Generate a summary or ask questions.</small></div>
            <div><strong>4. Grounding</strong><br><small>Answers include page citations.</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 6. Sidebar UI
with st.sidebar:
    st.subheader("Knowledge Base", divider="orange")
    uploaded_file = st.file_uploader("Select Research PDF", type="pdf", key="pdf_uploader")
    
    if uploaded_file:
        temp_path = os.path.join("data", uploaded_file.name)
        if not os.path.exists("data"): os.makedirs("data")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Index Document", icon=":material/database_upload:", use_container_width=True):
            with st.spinner("Processing PDF..."):
                try:
                    chunks = process_pdf(temp_path)
                    st.session_state.current_chunks = chunks
                    
                    vector_store = get_vector_store()
                    
                    # Use a notification to show we are clearing
                    with st.status("Preparing database...", expanded=False) as status:
                        try:
                            # Attempt to clear with a timeout safety net
                            vector_store.clear()
                            status.update(label="Database ready!", state="complete")
                        except Exception as e:
                            # If it times out, we'll try to delete and recreate 
                            # which is sometimes faster for the API
                            st.warning("Database response slow. Attempting alternative connection...")
                            vector_store.delete_collection()
                            vector_store = get_vector_store()
                    
                    vector_store.add_documents(chunks)
                    st.success("Indexed Successfully", icon=":material/check_circle:")
                except Exception as outer_e:
                    st.error(f"Connection Error: {str(outer_e)}")

    if st.session_state.current_chunks:
        st.divider()
        st.markdown('<div class="green-button">', unsafe_allow_html=True)
        if st.button("One page Summary", icon=":material/summarize:", use_container_width=True):
            with st.spinner("Synthesizing..."):
                summary = generate_summary(st.session_state.current_chunks)
                st.session_state.messages.append({"role": "assistant", "content": f"### Executive Summary\n{summary}"})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="red-button">', unsafe_allow_html=True)
    if st.button("Reset Database", icon=":material/delete_forever:", use_container_width=True):
        get_vector_store().clear()
        st.toast("Database Cleared")
        
    if st.button("Clear History", icon=":material/chat_bubble_outline:", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 7. Chat Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            sources_html = "".join([f'<span class="source-tag">{s}</span>' for s in message["sources"]])
            st.markdown(sources_html, unsafe_allow_html=True)

# 8. Chat Input
if prompt := st.chat_input("Ask a question about the document...", key="main_chat"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing context..."):
            context, sources = get_relevant_context_with_sources(prompt)
            answer = generate_answer(prompt, context)
            st.markdown(answer)
            if sources:
                sources_html = "".join([f'<span class="source-tag">{s}</span>' for s in sources])
                st.markdown(sources_html, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})