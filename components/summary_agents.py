import os
from typing import Optional
from dataclasses import dataclass
from groq import Groq
import google.generativeai as genai
from google.generativeai import GenerativeModel
import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

@dataclass
class Summary:
    long_summary: str
    short_summary: str

class GroqAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ API key not found in environment variables")
        self.client = Groq(api_key=self.api_key)
        self.max_chunk_tokens = 5000  # Safe limit below the 6000 TPM limit
    
    def split_text_into_chunks(self, text: str) -> list[str]:
        """Split text into chunks based on approximate token count."""
        # Rough approximation: 1 token ≈ 4 characters
        chars_per_chunk = self.max_chunk_tokens * 4
        
        # Split into sentences first (crude approach)
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > chars_per_chunk:
                # Join current chunk and add to chunks
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks
    
    def generate_long_summary(self, text: str) -> str:
        try:
            with st.spinner("Generating detailed summary..."):
                # Split text into chunks
                chunks = self.split_text_into_chunks(text)
                
                if len(chunks) == 1:
                    # If only one chunk, process it directly
                    prompt = f"""Please provide a detailed summary of the following text. 
                    Focus on key points, main arguments, and important details:
                    
                    {chunks[0]}
                    """
                    
                    completion = self.client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="deepseek-r1-distill-llama-70b",
                        temperature=0.3,
                        max_tokens=2048,
                    )
                    
                    return completion.choices[0].message.content
                
                # For multiple chunks, process them in a single prompt
                formatted_chunks = "\n\n".join([f"Part {i+1}:\n{chunk}" for i, chunk in enumerate(chunks)])
                
                prompt = f"""Please provide a coherent and detailed summary of the following text which is split into parts. 
                Consider all parts together and create a unified summary focusing on key points and main arguments:

                {formatted_chunks}
                """
                
                completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="deepseek-r1-distill-llama-70b",
                    temperature=0.3,
                    max_tokens=2048,
                )
                
                return completion.choices[0].message.content
                
        except Exception as e:
            st.error(f"Error generating long summary: {str(e)}")
            return ""

# Add or modify the Gemini API configuration
GEMINI_MAX_TOKENS = 8192

class GeminiAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found in environment variables")
        genai.configure(api_key=self.api_key)
        self.model = GenerativeModel('gemini-pro', 
                                    generation_config={
                                        'max_output_tokens': GEMINI_MAX_TOKENS,
                                        'temperature': 0.7
                                    })
    
    async def generate_short_summary(self, long_summary: str) -> str:
        try:
            with st.spinner("Generating concise summary..."):
                prompt = f"""Based on the following detailed summary, please create a shorter, 
                more concise version that captures the most essential points in a few paragraphs:
                
                {long_summary}
                """
                
                response = await self.model.generate_content_async(prompt)
                return response.text
        except Exception as e:
            st.error(f"Error generating short summary: {str(e)}")
            return ""

class SummaryOrchestrator:
    def __init__(self):
        self.groq_agent = GroqAgent()
        self.gemini_agent = GeminiAgent()
    
    async def generate_summaries(self, text: str) -> Summary:
        try:
            # Changed to synchronous call for Groq
            long_summary = self.groq_agent.generate_long_summary(text)
            if long_summary:
                short_summary = await self.gemini_agent.generate_short_summary(long_summary)
                return Summary(long_summary=long_summary, short_summary=short_summary)
            return Summary(long_summary="", short_summary="")
        except Exception as e:
            st.error(f"Error in summary generation pipeline: {str(e)}")
            return Summary(long_summary="", short_summary="")