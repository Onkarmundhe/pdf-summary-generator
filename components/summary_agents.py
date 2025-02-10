import os
from typing import Optional
from dataclasses import dataclass
from groq import Groq
import google.generativeai as genai
from google.generativeai import GenerativeModel
import streamlit as st
from dotenv import load_dotenv

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
    
    def generate_long_summary(self, text: str) -> str:
        try:
            with st.spinner("Generating detailed summary..."):
                prompt = f"""Please provide a detailed summary of the following text. 
                Focus on key points, main arguments, and important details:
                
                {text}
                """
                
                # Changed to synchronous call
                completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="deepseek-r1-distill-llama-70b",
                    temperature=0.3,
                    max_tokens=4096,
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