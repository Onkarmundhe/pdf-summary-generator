import streamlit as st

def show_header():
    """Display the application header."""
    st.markdown(
        """
        <h1 class='main-header'>PDF Summary Generator</h1>
        <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
            Upload your PDF and get AI-powered summaries using Groq and Gemini
        </p>
        """,
        unsafe_allow_html=True
    )