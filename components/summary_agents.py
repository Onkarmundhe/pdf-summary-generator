# summary_agents.py
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
        self.api_key = st.secrets["GROQ_API_KEY"]
        if not self.api_key:
            raise ValueError("GROQ API key not found in environment variables")
        self.client = Groq(api_key=self.api_key)
        self.max_chunk_tokens = 2000  # Reduced from 5000

    def split_text_into_chunks(self, text: str) -> list[str]:
        chars_per_chunk = self.max_chunk_tokens * 3  # Conservative estimate
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > chars_per_chunk:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        return chunks

    def generate_long_summary(self, text: str) -> str:
        try:
            with st.spinner("Generating detailed summary..."):
                chunks = self.split_text_into_chunks(text)
                chunk_summaries = []
                progress_bar = st.progress(0)

                for i, chunk in enumerate(chunks):
                    progress = (i + 1) / len(chunks)
                    progress_bar.progress(progress)
                    st.info(f"Processing part {i+1} of {len(chunks)}...")

                    prompt = f"Please provide a very brief summary of this text segment in 2-3 sentences:\n{chunk}"

                    if i > 0:
                        time.sleep(3)  # Rate limit handling

                    max_retries = 3
                    for retry in range(max_retries):
                        try:
                            completion = self.client.chat.completions.create(
                                messages=[{"role": "user", "content": prompt}],
                                model="deepseek-r1-distill-llama-70b",
                                temperature=0.3,
                                max_tokens=500
                            )
                            chunk_summaries.append(completion.choices[0].message.content)
                            break
                        except Exception as chunk_error:
                            if retry < max_retries - 1:
                                st.warning(f"Error processing chunk {i+1}. Retrying after delay...")
                                time.sleep(5 * (retry + 1))  # Exponential backoff
                            else:
                                st.error(f"Failed to process chunk {i+1} after {max_retries} attempts")

                progress_bar.empty()

                if not chunk_summaries:
                    return "Failed to generate summary due to processing errors."

                # Combine summaries in batches
                if len(chunk_summaries) > 1:
                    batch_size = 5
                    final_summaries = []

                    for i in range(0, len(chunk_summaries), batch_size):
                        batch = chunk_summaries[i:i + batch_size]
                        combined_batch = " ".join(batch)
                        st.info(f"Combining summary batch {(i//batch_size) + 1}...")
                        time.sleep(3)

                        batch_prompt = f"Create a coherent summary from these segment summaries in 2-3 sentences:\n{combined_batch}"

                        try:
                            batch_completion = self.client.chat.completions.create(
                                messages=[{"role": "user", "content": batch_prompt}],
                                model="deepseek-r1-distill-llama-70b",
                                temperature=0.3,
                                max_tokens=500
                            )
                            final_summaries.append(batch_completion.choices[0].message.content)
                        except Exception as batch_error:
                            st.warning(f"Error processing batch {(i//batch_size) + 1}. Skipping...")
                            continue

                    if len(final_summaries) > 1:
                        final_text = " ".join(final_summaries)
                        final_prompt = f"Create a final coherent summary from these summaries:\n{final_text}"
                        time.sleep(3)

                        final_completion = self.client.chat.completions.create(
                            messages=[{"role": "user", "content": final_prompt}],
                            model="deepseek-r1-distill-llama-70b",
                            temperature=0.3,
                            max_tokens=1000
                        )
                        return final_completion.choices[0].message.content

                    return final_summaries[0]
                return chunk_summaries[0]

        except Exception as e:
            st.error(f"Error generating long summary: {str(e)}")
            return ""

class GeminiAgent:
    def __init__(self):
        self.api_key = st.secrets["GEMINI_API_KEY"]
        if not self.api_key:
            raise ValueError("Gemini API key not found in environment variables")
        genai.configure(api_key=self.api_key)
        self.model = GenerativeModel('gemini-2.0-flash',
                                   generation_config={
                                       'max_output_tokens': 8192,
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
            max_retries = 3
            retry_delay = 60

            for attempt in range(max_retries):
                try:
                    long_summary = self.groq_agent.generate_long_summary(text)
                    if long_summary:
                        short_summary = await self.gemini_agent.generate_short_summary(long_summary)
                        return Summary(long_summary=long_summary, short_summary=short_summary)
                except Exception as e:
                    if attempt < max_retries - 1:
                        st.warning(f"Attempt {attempt + 1} failed. Retrying after delay...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        st.error(f"Failed after {max_retries} attempts: {str(e)}")

            return Summary(long_summary="", short_summary="")
        except Exception as e:
            st.error(f"Error in summary generation pipeline: {str(e)}")
            return Summary(long_summary="", short_summary="")
