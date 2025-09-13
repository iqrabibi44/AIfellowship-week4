import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from huggingface_hub import InferenceClient
import time

st.set_page_config(page_title="Model Comparison: Gemini vs Hugging Face", page_icon="📰")
st.title("📰 News Summarizer & Q&A — Gemini vs Hugging Face")

# ---- Sidebar: Keys and settings ----
st.sidebar.header("🔑 API Keys")
gemini_key = st.sidebar.text_input("Gemini API key", type="password")
hf_token   = st.sidebar.text_input("Hugging Face token", type="password")

temperature = st.sidebar.slider("Gemini creativity (temperature)", 0.0, 1.0, 0.7, 0.1)

if not gemini_key or not hf_token:
    st.warning("Please enter both API keys in the sidebar.")
    st.stop()

genai.configure(api_key=gemini_key)
gemini = genai.GenerativeModel("gemini-1.5-flash")
hf_client = InferenceClient(token=hf_token)

# ---- Input: Article URL ----
url = st.text_input("Enter a news article URL:")

import re

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ipv4
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None

if url:
    if not is_valid_url(url):
        st.warning("Please enter a valid URL starting with http:// or https://")
        st.stop()
    try:
        # --- Fetch article ---
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        article_text = " ".join(paragraphs).strip()

        if not article_text:
            st.warning("No article text found.")
            st.stop()

        st.subheader("Original Article Length")
        st.write(f"{len(article_text.split())} words")

        # ---- Gemini summary ----
        st.subheader("Gemini Summary")
        start = time.time()
        g_resp = gemini.generate_content(
            "Summarize in 3–4 sentences:\n\n" + article_text,
            generation_config={"temperature": temperature}
        )
        g_time = time.time() - start
        st.write(g_resp.text)
        st.caption(f"Gemini response time: {g_time:.2f} sec")

        # ---- Hugging Face BART summary ----
        st.subheader("Hugging Face BART Summary")
        start = time.time()
        bart_summary = hf_client.summarization(
            article_text,
            model="facebook/bart-large-cnn"
        )
        hf_time = time.time() - start
        st.write(bart_summary["summary_text"])
        st.caption(f"Hugging Face response time: {hf_time:.2f} sec")

        # ---- Q&A section ----
        st.subheader("💬 Ask a Question About the Article")
        question = st.text_input("Type your question:")

        if question:
            # Gemini answer
            g_qna = gemini.generate_content(
                f"Based on this article:\n\n{article_text}\n\nQuestion: {question}\nAnswer clearly."
            )

            # Falcon (open-weight model) for Q&A
            falcon_qna = hf_client.text_generation(
                model="tiiuae/falcon-7b-instruct",
                inputs=f"Answer the question based on the text:\n\n{article_text}\n\nQuestion: {question}\nAnswer:",
                parameters={"max_new_tokens":150, "do_sample":False}
            )

            st.markdown("**Gemini Answer:**")
            st.write(g_qna.text)
            st.markdown("**Hugging Face (Falcon-7B) Answer:**")
            st.write(falcon_qna)

    except Exception as e:
        if "403" in str(e) or "Forbidden" in str(e):
            st.error("403 Forbidden: Your Hugging Face token does not have sufficient permissions to access the inference API or the requested model. Please check your token scopes and generate a new token with the required permissions.")
        else:
            st.error(f"Error: {e}")
