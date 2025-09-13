# 📰 News Summarizer & Q\&A — Gemini vs Hugging Face

A Streamlit web app that compares **Gemini** and **Hugging Face BART** for news summarization and allows you to **ask questions** about the article.

---

## 🚀 Features

* Fetches a news article from any URL.
* Shows the **original word count**.
* Generates **two summaries**:

  * **Gemini** summary (Google Gemini API)
  * **Hugging Face BART** summary
* Lets you **ask a custom question** about the article.
* Displays **response times** for both models.

---

## 🛠️ Setup & Run Locally

1️⃣ **Clone the repository**

```bash
git clone <repo-url>
cd <repo-folder>
```

2️⃣ **Create and activate a virtual environment** (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

4️⃣ **Add your API keys**
Create a file `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "your_gemini_key"
HF_TOKEN = "your_huggingface_key"
```

5️⃣ **Run the app**

```bash
streamlit run app.py
```

The app will open in your browser (default: `http://localhost:8501`).

---

## 📦 Tech Stack

* **Python**, **Streamlit**
* **Google Gemini API**
* **Hugging Face Transformers (BART)**

---

