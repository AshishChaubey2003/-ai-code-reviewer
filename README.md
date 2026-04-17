# ⚡ AI Code Reviewer

> An agentic Python code review assistant powered by **Groq (Llama 3 70B)**, **LangGraph**, **LangChain**, **RAG**, and **FAISS** — get instant bug detection, auto-fixes, security audits, and performance feedback on your Python code.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Pipeline-blueviolet)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Llama3_70B-orange)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red)](https://streamlit.io)

---

## 🚀 Live Demo

👉 **[Click here to try it live](#)** ← *(https://aujd96shly6j3xw4w2otw7.streamlit.app/)*

---

## 📌 What It Does

AI Code Reviewer uses a **5-node LangGraph agentic pipeline** to deeply analyze your Python code:

| Feature | Description |
|---|---|
| 🐛 **Bug Detection** | Finds errors and logical issues with severity scoring |
| 🔁 **Auto-Fix Loop** | Automatically fixes bugs and re-analyzes (up to 3 attempts) |
| 🔐 **Security Audit** | Checks for OWASP Top 10 — SQL injection, hardcoded secrets, eval/exec abuse, path traversal, and more |
| ⚡ **Performance Review** | Detects bottlenecks, missing caching, unnecessary loops |
| 📖 **Code Quality** | PEP8 violations, naming conventions, error handling, duplication |
| 📚 **RAG-Powered** | Upload your own PDF coding guidelines for personalized review |
| 📊 **Scored Report** | Bug, Security, and Quality scores (0–10) with a full downloadable report |

---

## 🧠 Agent Architecture

The core of this project is a **LangGraph state machine** with a conditional auto-fix loop:

```
User Code + (Optional PDF Guidelines)
            │
            ▼
    ┌─── ANALYZE BUGS ◄────────────────────┐
    │         │                            │
    │    bugs found?                       │
    │    ┌────┴─────┐                      │
    │  YES (& attempts < 3)   NO           │
    │    ▼                    │            │
    │  AUTO-FIX ──────────────┘ (loop)     │
    └──────────────────────────────────────┘
                 │
                 ▼
          SECURITY AUDIT
                 │
                 ▼
         QUALITY REVIEW
                 │
                 ▼
        GENERATE REPORT
```

### The 5 Nodes

| Node | Role |
|---|---|
| `analyze_bugs_node` | Detects bugs + assigns severity score (0–10) |
| `auto_fix_node` | Rewrites buggy code, increments fix attempt counter |
| `security_node` | OWASP Top 10 audit + security score |
| `quality_node` | Performance, PEP8, naming, error handling review |
| `report_node` | Assembles final markdown report with all scores |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Groq API** | Ultra-fast LLM inference (LPU hardware) |
| **Llama 3 70B** | Open-source state-of-the-art model |
| **LangGraph** | Agentic pipeline with conditional loops |
| **LangChain** | Prompt management and chain orchestration |
| **FAISS** | Local vector database for RAG |
| **HuggingFace Embeddings** | `all-MiniLM-L6-v2` — free, no API key needed |
| **Streamlit** | UI with dark/light theme toggle |
| **PyPDF** | PDF ingestion for RAG knowledge base |
| **python-dotenv** | Secure API key management |

---

## ⚙️ How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/AshishChaubey2003/-ai-code-reviewer.git
cd -ai-code-reviewer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key → [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, main file `app.py`
4. Add your secret: **Settings → Secrets**
   ```
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **Deploy** — done!

---

## 📁 Project Structure

```
ai-code-reviewer/
├── app.py              # Streamlit UI — dark/light theme, layout, controls
├── agent_graph.py      # LangGraph pipeline — nodes, edges, fix loop logic
├── agent_nodes.py      # 5 agent nodes — analyze, fix, security, quality, report
├── agent_state.py      # TypedDict state shared across all nodes
├── reviewer.py         # Simple single-pass reviewer (legacy)
├── rag_pipeline.py     # FAISS vector store + similarity search
├── embeddings.py       # HuggingFace embeddings config
├── requirements.txt    # All dependencies
├── .env                # API keys (not committed)
└── README.md
```

---

## ✨ UI Features

- 🌙☀️ **Dark / Light theme toggle**
- ✏️ **Paste code** or **upload a `.py` file**
- 📚 **Upload PDF guidelines** to build a RAG knowledge base
- 🔍 **Agent execution trace** — see which nodes ran and how many fix loops occurred
- 📊 **Score cards** — Bug Severity, Security, Quality scores at a glance
- 💾 **Download report** as `.txt`
- ⬇️ **Download fixed code** as `.py`
- 📈 **Session review counter**

---

## 👨‍💻 Author

**Ashish Kumar Chaubey**
- GitHub → [AshishChaubey2003](https://github.com/AshishChaubey2003)
- LinkedIn → *(https://www.linkedin.com/in/ashishchaubey2dec/)*

---

> Built as part of my GenAI learning journey — exploring LangGraph agents, RAG pipelines, and production-grade AI app development. 🚀
