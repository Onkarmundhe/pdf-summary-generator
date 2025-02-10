import streamlit as st

def show_footer():
    """Display the footer with app information."""
    st.markdown(
        """
        <div class="footer">
            <p style='font-size: 0.8rem; color: #666;'>
                Built with Streamlit ❤️
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )