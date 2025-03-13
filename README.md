# PDF Summary Generator 📄

A Streamlit-based web application that generates concise summaries of PDF documents using Groq and Gemini AI models.

🔗 [Live Demo](https://pdf-summary-generator-mippvhd8j3oqhpvgmaxuwi.streamlit.app)

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 📤 Easy PDF upload interface
- 📝 Extracts text from PDF documents
- 🤖 Generates both detailed and concise summaries
- 🎨 Clean and intuitive user interface
- ⚡ Powered by Groq and Gemini AI models

## Prerequisites

- Python 3.11 or higher
- Groq API key ([Get it here](https://console.groq.com))
- Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-summary-generator.git
   cd pdf-summary-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy environment templates
   cp .env.example .env
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

5. Update the following files with your API keys:
   - `.env`
   - `.streamlit/secrets.toml`

6. Run the application:
   ```bash
   streamlit run app.py
   ```

7. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```


## Project Structure

```
pdf-summary-generator/
├── .streamlit/
│   ├── secrets.toml
│   └── secrets.toml.example
├── assets/
│   └── logo.png
├── components/
│   └── summary_agents.py
├── styles/
│   └── main.css
├── utils/
│   ├── footer.py
│   ├── header.py
│   ├── pdf_processor.py
│   └── styles.py
├── .env
├── .env.example
├── .gitignore
├── README.md
├── app.py
└── requirements.txt
```

## Usage

1. Access the application through your web browser
2. Upload a PDF file using the file upload interface
3. Click "Generate Summary" to process the document
4. View both concise and detailed summaries of your document

## API Rate Limits

- Groq API: Refer to [Groq's pricing page](https://console.groq.com/pricing) for current limits
- Gemini API: Refer to [Google AI Studio](https://makersuite.google.com/app/apikey) for quota information




