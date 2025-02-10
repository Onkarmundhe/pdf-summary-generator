import streamlit as st
import asyncio
from utils.pdf_processor import PDFProcessor
from utils.styles import apply_custom_styles, show_success_message
from utils.header import show_header
from utils.footer import show_footer
from components.summary_agents import SummaryOrchestrator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Summary Generator",
    page_icon="📄",
    layout="wide",
)

# Apply custom styles
apply_custom_styles()

def load_css():
    with open('styles/main.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

async def main():
    # Load CSS first
    load_css()
    
    # Show header
    show_header()
    
    # Initialize components
    pdf_processor = PDFProcessor()
    summary_orchestrator = SummaryOrchestrator()

    # File upload
    uploaded_file = st.file_uploader(
        "Upload your PDF file",
        type=["pdf"],
        help="Upload a PDF file to generate its summary"
    )

    if uploaded_file is not None:
        if pdf_processor.validate_pdf(uploaded_file):
            # Add generate button
            if st.button("Generate Summary", type="primary"):
                # Extract text from PDF
                text = pdf_processor.extract_text(uploaded_file)
                
                if text:
                    # Generate summaries
                    summaries = await summary_orchestrator.generate_summaries(text)
                    
                    if summaries.short_summary:
                        show_success_message()
                        
                        # Display the final summary
                        st.markdown("<h2 class='sub-header'>Summary</h2>", unsafe_allow_html=True)
                        
                        # Display summary in a container with proper formatting
                        st.markdown(
                            f"""<div class='summary-container'>
                                <div class='summary-text'>{summaries.short_summary}</div>
                            </div>""",
                            unsafe_allow_html=True
                        )
                        
                        # Add option to view detailed summary
                        with st.expander("View detailed summary"):
                            st.markdown(
                                f"<div class='summary-text'>{summaries.long_summary}</div>",
                                unsafe_allow_html=True
                            )
    
    # Show footer
    show_footer()

if __name__ == "__main__":
    asyncio.run(main())