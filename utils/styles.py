import streamlit as st

def apply_custom_styles():
    """Apply custom styles to the Streamlit app."""
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: 500;
            color: #424242;
            margin-bottom: 1rem;
        }
        .summary-container {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin: 1rem 0;
            color: #333;  /* Added explicit text color */
            font-size: 1rem;  /* Added explicit font size */
            line-height: 1.6;  /* Added line height for better readability */
        }
        .summary-text {
            color: #333;
            font-size: 1rem;
            line-height: 1.6;
            white-space: pre-wrap;  /* Preserve line breaks */
            font-family: sans-serif;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f8f9fa;
            padding: 1rem;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)

def show_success_message():
    """Show success message with custom styling."""
    st.markdown("""
        <div style='
            padding: 1rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            color: #155724;
            margin: 1rem 0;
        '>
            Summary generated successfully!
        </div>
    """, unsafe_allow_html=True)