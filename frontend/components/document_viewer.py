import streamlit as st
import pandas as pd

def document_viewer(documents: list):
    """Component for viewing and searching documents"""
    st.subheader("Document Explorer")
    
    # Search box
    search_term = st.text_input("Search within documents")
    
    # Document selection
    selected_doc = st.selectbox(
        "Select document to view",
        options=[doc["filename"] for doc in documents],
        index=0
    )
    
    # Display document content
    doc = next(d for d in documents if d["filename"] == selected_doc)
    
    if search_term:
        # Highlight search term in content
        highlighted = doc["text"].replace(
            search_term, 
            f"<span class='highlight'>{search_term}</span>"
        )
        st.markdown(f"<div class='doc-content'>{highlighted}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='doc-content'>{doc['text']}</div>", unsafe_allow_html=True)
    
    # Show metadata
    with st.expander("Document Metadata"):
        st.json(doc.get("metadata", {}))