import streamlit as st

def show_header():
    """Display the application header."""
    # Create two columns for logo and title
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image("assets/logo.png", width=80)
    
    with col2:
        st.markdown("<h1 style='margin-top: 15px;'>PDF Summary Generator</h1>", unsafe_allow_html=True)