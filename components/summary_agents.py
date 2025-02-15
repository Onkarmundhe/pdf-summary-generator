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
        """Split text into smaller chunks to respect token limits."""
        # Reduce chunk size for safer processing
        self.max_chunk_tokens = 2000  # Significantly reduced from 5000
        chars_per_chunk = self.max_chunk_tokens * 3  # More conservative estimate
        
        # Split into sentences
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
                chunk_summaries = []
                
                # Process chunks with progress bar
                progress_bar = st.progress(0)
                for i, chunk in enumerate(chunks):
                    # Show progress
                    progress = (i + 1) / len(chunks)
                    progress_bar.progress(progress)
                    st.info(f"Processing part {i+1} of {len(chunks)}...")
                    
                    # Process smaller chunks
                    prompt = f"""Please provide a brief summary of this text segment:
                    
                    {chunk}
                    """
                    
                    # Add delay between chunks to respect rate limits
                    if i > 0:
                        time.sleep(3)  # 3 second delay between chunks
                    
                    try:
                        completion = self.client.chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model="deepseek-r1-distill-llama-70b",
                            temperature=0.3,
                            max_tokens=1000,  # Reduced token limit for safety
                        )
                        chunk_summaries.append(completion.choices[0].message.content)
                    except Exception as chunk_error:
                        st.warning(f"Error processing chunk {i+1}. Retrying after delay...")
                        time.sleep(5)  # Longer delay on error
                        continue
                
                # Clear progress
                progress_bar.empty()
                
                if not chunk_summaries:
                    return "Failed to generate summary due to processing errors."
                
                # Combine summaries in smaller batches if needed
                if len(chunk_summaries) > 1:
                    combined_text = " ".join(chunk_summaries)
                    final_prompt = f"""Create a coherent summary from these segment summaries:

                    {combined_text}
                    """
                    
                    # Final summary with reduced tokens
                    final_completion = self.client.chat.completions.create(
                        messages=[{"role": "user", "content": final_prompt}],
                        model="deepseek-r1-distill-llama-70b",
                        temperature=0.3,
                        max_tokens=1500,
                    )
                    
                    return final_completion.choices[0].message.content
                
                return chunk_summaries[0]
                
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