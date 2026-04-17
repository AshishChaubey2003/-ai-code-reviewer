# 🔍 AI Code Reviewer

> An intelligent code review assistant powered by Groq (Llama 3 70B), LangChain, RAG, and FAISS — built for developers who want instant, expert-level feedback on their Python code.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Llama3_70B-orange)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red)](https://streamlit.io)

---

## 🚀 Live Demo
👉 **[Click here to try it live](#)** ← (Streamlit Cloud link yahan daalna)

---

## 📌 What It Does

AI Code Reviewer analyzes your Python code and provides:

- 🐛 **Bug Detection** — Finds errors and logical issues
- 🔐 **Security Audit** — Identifies vulnerabilities
- ⚡ **Performance Review** — Suggests optimizations
- 📖 **Best Practices** — PEP8 and clean code tips
- ✅ **Improved Code** — Gives a refactored version
- 📚 **RAG-Powered** — Upload your own coding guidelines for personalized review

---

## 🛠️ Tech Stack

| Technology | Purpose | Why I Chose It |
|---|---|---|
| **Python** | Core language | Industry standard for AI/backend |
| **Groq API** | LLM inference | 10x faster than GPU, free tier available |
| **Llama 3 70B** | AI Model | Open-source SOTA, no vendor lock-in |
| **LangChain** | Orchestration | Clean prompt management + RAG pipeline |
| **FAISS** | Vector Database | Meta's production-grade, no external service needed |
| **HuggingFace Embeddings** | Text → Vector | Free, no API key required |
| **Streamlit** | UI Framework | Rapid AI app development |
| **Streamlit Cloud** | Deployment | Auto CI/CD via GitHub push |
| **PyPDF2** | PDF Parser | Upload coding guidelines/docs |
| **python-dotenv** | Security | Safe API key management |

---

## 🧠 Architecture

```
User Input (Code + Optional PDF Guidelines)
            ↓
    PDF → PyPDF2 → Text Chunks
            ↓
    HuggingFace Embeddings → FAISS Vector Store
            ↓
    RAG Pipeline (Similarity Search)
            ↓
    LangChain Prompt Template
            ↓
    Groq API (Llama 3 70B) — Ultra Fast Inference
            ↓
    Structured Code Review Output
```

---

## ⚙️ How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/AshishChaubey2003/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
# Create .env file
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key → https://console.groq.com

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ai-code-reviewer/
├── app.py              # Streamlit UI (Dark/Light theme toggle)
├── reviewer.py         # Groq + LangChain review logic
├── rag_pipeline.py     # FAISS + RAG setup
├── embeddings.py       # HuggingFace embeddings
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
├── .gitignore
└── README.md
```

---

## ✨ Key Features

- 🌙☀️ **Dark/Light theme toggle**
- 📁 **Upload .py file** or paste code directly
- 📚 **RAG support** — upload PDF coding guidelines
- 💾 **Download review** as text file
- 📊 **Review stats** — track how many reviews done
- ⚡ **Ultra fast** — Groq LPU inference

---

## 👨‍💻 Author

**Ashish Kumar Chaubey**
- GitHub → [AshishChaubey2003](https://github.com/AshishChaubey2003)
- LinkedIn → [Your LinkedIn](#)

---

## 📌 Note

> Built as part of my GenAI learning journey — exploring LangChain, RAG, and production-grade AI app development. 🚀# -ai-code-reviewer
AI-powered Python code reviewer using Groq (Llama 3), LangChain, RAG &amp; FAISS — get instant bug detection, security audit &amp; code improvements with your own documentation context.
