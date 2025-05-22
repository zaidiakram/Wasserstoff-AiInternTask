import streamlit as st

def citation_manager(citations: list):
    """Component for managing and displaying citations"""
    if not citations:
        st.info("No citations available")
        return
    
    # Group citations by document
    citation_groups = {}
    for citation in citations:
        doc_name = citation["source"]
        if doc_name not in citation_groups:
            citation_groups[doc_name] = []
        citation_groups[doc_name].append(citation)
    
    # Display citations in tabs
    tabs = st.tabs(list(citation_groups.keys()))
    
    for tab, (doc_name, doc_citations) in zip(tabs, citation_groups.items()):
        with tab:
            st.subheader(f"Citations from {doc_name}")
            for cite in doc_citations:
                with st.expander(f"Page {cite.get('page', 'N/A')}, Paragraph {cite.get('paragraph', 'N/A')}"):
                    st.markdown(f"**Relevance Score**: {cite.get('score', 0):.2f}")
                    st.markdown("**Text Excerpt**:")
                    st.markdown(f"> {cite.get('text', '')}")
                    st.markdown(f"**Location**: {cite.get('location', '')}")