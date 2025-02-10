import streamlit as st

def show_footer():
    """Display the footer with app information."""
    st.markdown(
        """
        <div class="footer">
            <p style='font-size: rem; color: #666;'>
                <br/>
                <span style='font-size: 1 rem;'>
                    Built with Streamlit ❤️
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )