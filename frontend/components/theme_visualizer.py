import streamlit as st
import pandas as pd
import plotly.express as px

def theme_visualizer(conversation: list):
    """Component for visualizing identified themes"""
    st.subheader("Theme Analysis Across Documents")
    

    themes = []
    for msg in conversation:
        if msg.get("themes"):
            themes.append({
                "query": msg["content"],
                "themes": msg["themes"]
            })
    
    if not themes:
        st.info("No themes identified yet. Ask questions to discover themes.")
        return
    

    st.plotly_chart(
        px.sunburst(
            pd.DataFrame(themes),
            path=["query", "themes"],
            title="Theme Relationship Map"
        ),
        use_container_width=True
    )
    
    
    st.subheader("Theme Breakdown")
    for theme in themes:
        with st.expander(f"Themes for: '{theme['query']}'"):
            st.write(theme["themes"])