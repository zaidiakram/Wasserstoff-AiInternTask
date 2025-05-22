import streamlit as st
from components.document_viewer import document_viewer
from components.theme_visualizer import theme_visualizer
from components.citation_manager import citation_manager
from utils.api_client import DocumentClient
import base64
import os

st.set_page_config(
    page_title="Wasserstoff Gen-AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/styles.css")


client = DocumentClient("http://localhost:8080")

def main():
    st.title("📄 Document Research & Theme Identification Chatbot")
    st.markdown("Upload documents or scanned images, ask questions, and identify common themes across your research corpus.")
    
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "processed_docs" not in st.session_state:
        st.session_state.processed_docs = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    
    with st.sidebar:
        st.header("Document Management")
        uploaded_files = st.file_uploader(
            "Upload research documents (PDF, DOCX, TXT, JPG, PNG)",
            type=["pdf", "docx", "txt", "jpg", "jpeg", "png"],
            accept_multiple_files=True
        )
        
        if st.button("Process Documents", help="Extract text via NLP or OCR and build search index"):
            with st.spinner("Processing documents..."):
                response = client.upload_files(uploaded_files)
                if response.get("success"):
                    st.session_state.processed_docs = response.get("documents", [])
                    st.success(f"Processed {len(response['documents'])} documents (including OCR if needed)")
                else:
                    st.error(f"Error: {response.get('error', 'Unknown error')}")

        st.divider()
        st.markdown("### Document Selection")
        if st.session_state.processed_docs:
            selected_docs = st.multiselect(
                "Filter documents for querying",
                options=[doc["filename"] for doc in st.session_state.processed_docs],
                default=[doc["filename"] for doc in st.session_state.processed_docs]
            )
        else:
            st.info("Upload and process documents first")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["Chat Interface", "Document Viewer", "Theme Analysis"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        if st.session_state.processed_docs:
            document_viewer(st.session_state.processed_docs)
        else:
            st.warning("No documents available for viewing")
    
    with tab3:
        if st.session_state.conversation:
            theme_visualizer(st.session_state.conversation)
        else:
            st.info("Ask questions to identify themes across documents")

def chat_interface():
    """Main chat interface for querying documents"""
    st.subheader("Research Assistant")
    
    
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("citations"):
                with st.expander("View Citations"):
                    citation_manager(message["citations"])
            if message.get("themes"):
                with st.expander("Identified Themes"):
                    st.write(message["themes"])
    
    
    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing documents..."):
                response = client.ask_question(
                    prompt,
                    doc_filter=[doc["filename"] for doc in st.session_state.processed_docs]
                )
            
            if "error" in response:
                st.error(response["error"])
            else:
                st.markdown(response["answer"])
                
                if response.get("citations"):
                    with st.expander("View Citations"):
                        citation_manager(response["citations"])
                
                if response.get("themes"):
                    with st.expander("Identified Themes"):
                        st.write(response["themes"])
                
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "citations": response.get("citations", []),
                    "themes": response.get("themes", "")
                })

if __name__ == "__main__":
    main()
