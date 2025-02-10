import streamlit as st
import os

def show_header():
    """Display the application header."""
    # Create two columns for logo and title
    col1, col2 = st.columns([1, 4])
    
    with col1:
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
        else:
            st.warning("Logo not found")
    
    with col2:
        st.markdown("<h1 style='margin-top: 15px;'>PDF Summary Generator</h1>", unsafe_allow_html=True)