import streamlit as st
from reviewer import review_code
from rag_pipeline import create_vectorstore, get_relevant_context

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🔍",
    layout="wide"
)

# ✅ Theme Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ✅ Dynamic CSS based on theme
bg_main     = "#0f0f1a" if dark else "#f0f2f8"
bg_card     = "#1a1a2e" if dark else "#ffffff"
bg_sidebar  = "#121220" if dark else "#1a1a2e"
text_main   = "#e0e0ff" if dark else "#1a1a2e"
text_muted  = "#8888aa" if dark else "#555577"
accent      = "#00d4ff"
border      = "#2a2a4a" if dark else "#d0d4e8"
input_bg    = "#0d0d1f" if dark else "#f8f9ff"
code_bg     = "#0a0a18" if dark else "#f4f6ff"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Syne', sans-serif;
        background-color: {bg_main};
        color: {text_main};
    }}

    .main .block-container {{
        background-color: {bg_main};
        padding: 2rem 2rem 2rem 2rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar};
        border-right: 1px solid {border};
    }}
    section[data-testid="stSidebar"] * {{
        color: #e0e0ff !important;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, {accent}, #0099bb);
        color: #000 !important;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
        border: none;
        padding: 10px;
        margin: 4px 0;
        font-family: 'Syne', sans-serif;
        transition: 0.3s;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        opacity: 0.85;
        transform: scale(1.02);
    }}

    .stTextArea textarea {{
        background-color: {input_bg} !important;
        color: {text_main} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
    }}
    .stTextArea textarea:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
    }}

    .stButton > button {{
        background: linear-gradient(135deg, {accent}, #0077aa);
        color: #000 !important;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-family: 'Syne', sans-serif;
        font-size: 15px;
        transition: all 0.3s;
        letter-spacing: 0.3px;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,212,255,0.3);
    }}

    .stRadio label {{
        color: {text_main} !important;
        font-size: 14px;
    }}

    div[data-testid="stFileUploader"] {{
        background-color: {input_bg};
        border: 1px dashed {accent};
        border-radius: 12px;
        padding: 12px;
    }}

    .hero-title {{
        text-align: center;
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, {accent}, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: -1px;
    }}
    .hero-sub {{
        text-align: center;
        color: {text_muted};
        font-size: 14px;
        margin-bottom: 1.5rem;
        font-family: 'JetBrains Mono', monospace;
    }}

    .stat-card {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        margin-bottom: 12px;
    }}
    .stat-label {{
        font-size: 11px;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }}
    .stat-value {{
        font-size: 22px;
        font-weight: 800;
        color: {accent};
        font-family: 'JetBrains Mono', monospace;
    }}

    .section-header {{
        font-size: 15px;
        font-weight: 600;
        color: {text_main};
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid {border};
        padding-bottom: 8px;
    }}

    .review-output {{
        background: {code_bg};
        border: 1px solid {border};
        border-left: 3px solid {accent};
        border-radius: 12px;
        padding: 20px;
        font-size: 14px;
        line-height: 1.8;
        color: {text_main};
        font-family: 'Syne', sans-serif;
    }}

    .badge {{
        display: inline-block;
        background: rgba(0,212,255,0.12);
        color: {accent};
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px 2px;
        font-family: 'JetBrains Mono', monospace;
    }}

    .stAlert {{
        border-radius: 12px !important;
    }}

    hr {{
        border-color: {border} !important;
    }}

    .stSelectbox > div > div {{
        background-color: {input_bg} !important;
        color: {text_main} !important;
        border-color: {border} !important;
        border-radius: 10px !important;
    }}

    div[data-testid="stMetric"] {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 12px 16px;
    }}
    div[data-testid="stMetric"] label {{ color: {text_muted} !important; font-size: 12px; }}
    div[data-testid="stMetric"] div {{ color: {accent} !important; font-size: 22px; font-weight: 800; }}
    </style>
""", unsafe_allow_html=True)

# ✅ Session State
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "review" not in st.session_state:
    st.session_state.review = None
if "review_count" not in st.session_state:
    st.session_state.review_count = 0

# ✅ Sidebar
with st.sidebar:
    st.markdown("## 🔍 Code Reviewer")
    st.caption("Groq · LangChain · RAG · FAISS")
    st.divider()

    # Theme Toggle
    theme_label = "☀️ Switch to Light" if dark else "🌙 Switch to Dark"
    if st.button(theme_label):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()

    # Stats
    st.markdown("### 📊 Stats")
    st.metric("Reviews Done", st.session_state.review_count)
    rag_status = "✅ Ready" if st.session_state.vectorstore else "❌ Not loaded"
    st.metric("RAG Status", rag_status)

    st.divider()

    # RAG Upload
    st.markdown("### 📚 Upload Guidelines")
    st.caption("PDF docs / coding standards")
    uploaded_docs = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if uploaded_docs:
        if st.button("⚡ Process Documents"):
            with st.spinner("Building RAG knowledge base..."):
                st.session_state.vectorstore = create_vectorstore(uploaded_docs)
            st.success("✅ Knowledge base ready!")

    st.divider()
    st.markdown("### 🛠️ Tech Stack")
    techs = ["Groq LPU", "Llama 3 70B", "LangChain", "FAISS", "HuggingFace", "Streamlit"]
    for t in techs:
        st.markdown(f'<span class="badge">{t}</span>', unsafe_allow_html=True)

# ✅ Main UI
st.markdown('<div class="hero-title">🔍 AI Code Reviewer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Groq (Llama 3 70B) · LangChain · RAG · FAISS · Streamlit</div>',
    unsafe_allow_html=True
)
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-header">📝 Your Code</div>', unsafe_allow_html=True)

    input_method = st.radio(
        "Input method",
        ["✏️ Paste Code", "📁 Upload .py File"],
        horizontal=True,
        label_visibility="collapsed"
    )

    user_code = ""

    if input_method == "✏️ Paste Code":
        user_code = st.text_area(
            "Paste your Python code",
            height=380,
            placeholder="# Paste your Python code here...\ndef my_function():\n    pass",
            label_visibility="collapsed"
        )
    else:
        uploaded_code = st.file_uploader(
            "Upload .py file",
            type=["py"],
            label_visibility="collapsed"
        )
        if uploaded_code:
            user_code = uploaded_code.read().decode("utf-8")
            st.code(user_code, language="python")

    # Line count
    if user_code.strip():
        lines = len(user_code.strip().split("\n"))
        st.caption(f"📏 {lines} lines · {len(user_code)} characters")

    st.markdown("")
    if st.button("🚀 Review My Code", use_container_width=True):
        if user_code.strip():
            with st.spinner("🤖 Analyzing your code with Groq..."):
                context = get_relevant_context(
                    st.session_state.vectorstore,
                    user_code
                )
                review = review_code(user_code, context)
                st.session_state.review = review
                st.session_state.used_rag = bool(context)
                st.session_state.review_count += 1
        else:
            st.warning("⚠️ Please enter some code first!")

with col2:
    st.markdown('<div class="section-header">📊 Review Results</div>', unsafe_allow_html=True)

    if st.session_state.review:
        if st.session_state.get("used_rag"):
            st.success("✅ Review enhanced with your uploaded documentation!")
        else:
            st.info("💡 No guidelines uploaded — using general best practices.")

        st.markdown(
            f'<div class="review-output">{st.session_state.review}</div>',
            unsafe_allow_html=True
        )

        # Download button
        st.download_button(
            label="💾 Download Review",
            data=st.session_state.review,
            file_name="code_review.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.markdown(f"""
        <div style="
            background: {bg_card};
            border: 1px dashed {border};
            border-radius: 14px;
            padding: 60px 30px;
            text-align: center;
            color: {text_muted};
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">🔍</div>
            <div style="font-size: 16px; font-weight: 600; color: {text_main}; margin-bottom: 8px;">
                Ready to review your code
            </div>
            <div style="font-size: 13px;">
                Paste code on the left and click Review
            </div>
        </div>
        """, unsafe_allow_html=True)