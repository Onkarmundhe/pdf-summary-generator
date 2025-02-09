import PyPDF2
from io import BytesIO
import streamlit as st

class PDFProcessor:
    @staticmethod
    def validate_pdf(uploaded_file) -> bool:
        """Validate if the uploaded file is a PDF."""
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                return True
            else:
                st.error("Please upload a valid PDF file.")
                return False
        return False

    @staticmethod
    def extract_text(uploaded_file) -> str:
        """Extract text from uploaded PDF file."""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            st.error(f"Error extracting PDF text: {str(e)}")
            return ""