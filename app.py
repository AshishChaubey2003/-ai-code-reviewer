import streamlit as st
from reviewer import review_code
from rag_pipeline import create_vectorstore, get_relevant_context

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="⚡",
    layout="wide"
)

# ── Session State ──
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "review" not in st.session_state:
    st.session_state.review = None
if "review_count" not in st.session_state:
    st.session_state.review_count = 0

dark = st.session_state.dark_mode

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif !important;
    background: {'#060612' if dark else '#f0f2ff'} !important;
    color: {'#e8e8ff' if dark else '#0d0d2b'} !important;
}}

/* ── Animated background ── */
.main {{
    background: {'#060612' if dark else '#f0f2ff'} !important;
    position: relative;
}}
.main::before {{
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: {'radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.12) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.10) 0%, transparent 50%), radial-gradient(ellipse at 50% 50%, rgba(6,182,212,0.06) 0%, transparent 60%)' if dark else 'radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.08) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.06) 0%, transparent 50%)'};
    animation: bgShift 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}}
@keyframes bgShift {{
    0% {{ transform: translate(0, 0) rotate(0deg); }}
    100% {{ transform: translate(2%, 2%) rotate(1deg); }}
}}

.main .block-container {{
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 1;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {'rgba(10,10,30,0.95)' if dark else 'rgba(255,255,255,0.92)'} !important;
    border-right: 1px solid {'rgba(99,102,241,0.2)' if dark else 'rgba(99,102,241,0.15)'} !important;
    backdrop-filter: blur(20px);
}}
section[data-testid="stSidebar"] > div {{
    padding: 1.5rem 1rem !important;
}}
section[data-testid="stSidebar"] * {{
    color: {'#e8e8ff' if dark else '#0d0d2b'} !important;
}}

/* ── Sidebar brand ── */
.sidebar-brand {{
    text-align: center;
    padding: 1rem 0 0.5rem;
}}
.sidebar-logo {{
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.3rem;
    animation: pulse 3s ease-in-out infinite;
}}
@keyframes pulse {{
    0%, 100% {{ transform: scale(1); filter: drop-shadow(0 0 8px rgba(99,102,241,0.5)); }}
    50% {{ transform: scale(1.08); filter: drop-shadow(0 0 16px rgba(139,92,246,0.7)); }}
}}
.sidebar-title {{
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.sidebar-sub {{
    font-size: 0.7rem;
    color: {'#6b6b9a' if dark else '#7070a0'} !important;
    font-family: 'Fira Code', monospace;
    margin-top: 2px;
}}

/* ── Stat cards ── */
.stat-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 0.8rem 0;
}}
.stat-card {{
    background: {'rgba(99,102,241,0.08)' if dark else 'rgba(99,102,241,0.06)'};
    border: 1px solid {'rgba(99,102,241,0.2)' if dark else 'rgba(99,102,241,0.15)'};
    border-radius: 12px;
    padding: 10px 8px;
    text-align: center;
    transition: all 0.3s;
}}
.stat-card:hover {{
    border-color: rgba(99,102,241,0.5);
    transform: translateY(-2px);
}}
.stat-val {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #6366f1 !important;
    font-family: 'Fira Code', monospace;
    display: block;
    -webkit-text-fill-color: #6366f1 !important;
}}
.stat-lbl {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {'#6b6b9a' if dark else '#7070a0'} !important;
    margin-top: 2px;
    display: block;
    -webkit-text-fill-color: {'#6b6b9a' if dark else '#7070a0'} !important;
}}

/* ── Tech badges ── */
.badge-wrap {{ display: flex; flex-wrap: wrap; gap: 5px; margin-top: 6px; }}
.tech-badge {{
    background: {'rgba(99,102,241,0.1)' if dark else 'rgba(99,102,241,0.08)'};
    border: 1px solid {'rgba(99,102,241,0.25)' if dark else 'rgba(99,102,241,0.2)'};
    color: {'#a5b4fc' if dark else '#4f46e5'} !important;
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 0.68rem;
    font-family: 'Fira Code', monospace;
    font-weight: 500;
    -webkit-text-fill-color: {'#a5b4fc' if dark else '#4f46e5'} !important;
}}

/* ── Sidebar buttons ── */
section[data-testid="stSidebar"] .stButton button {{
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    width: 100% !important;
    padding: 10px !important;
    transition: all 0.3s !important;
    letter-spacing: 0.3px !important;
}}
section[data-testid="stSidebar"] .stButton button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
}}

/* ── Hero ── */
.hero-wrap {{
    text-align: center;
    padding: 0.5rem 0 1.2rem;
    position: relative;
}}
.hero-eyebrow {{
    font-size: 0.72rem;
    font-family: 'Fira Code', monospace;
    color: #6366f1;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    opacity: 0;
    animation: fadeUp 0.6s ease forwards 0.1s;
}}
.hero-title {{
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 40%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    opacity: 0;
    animation: fadeUp 0.6s ease forwards 0.2s;
}}
.hero-desc {{
    font-size: 0.85rem;
    color: {'#6b6b9a' if dark else '#7070a0'};
    font-family: 'Fira Code', monospace;
    margin-top: 0.5rem;
    opacity: 0;
    animation: fadeUp 0.6s ease forwards 0.35s;
}}
.hero-divider {{
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    margin: 1rem auto 0;
    border-radius: 2px;
    opacity: 0;
    animation: fadeUp 0.6s ease forwards 0.45s;
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* ── Glass panels ── */
.glass-panel {{
    background: {'rgba(15,15,40,0.6)' if dark else 'rgba(255,255,255,0.7)'};
    border: 1px solid {'rgba(99,102,241,0.18)' if dark else 'rgba(99,102,241,0.15)'};
    border-radius: 20px;
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: {'0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05)' if dark else '0 8px 32px rgba(99,102,241,0.08), inset 0 1px 0 rgba(255,255,255,0.8)'};
    transition: all 0.3s;
}}
.glass-panel:hover {{
    border-color: {'rgba(99,102,241,0.3)' if dark else 'rgba(99,102,241,0.25)'};
    box-shadow: {'0 12px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05)' if dark else '0 12px 40px rgba(99,102,241,0.12)'};
}}

.panel-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid {'rgba(99,102,241,0.15)' if dark else 'rgba(99,102,241,0.12)'};
}}
.panel-icon {{
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.2));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}}
.panel-title {{
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    color: {'#e8e8ff' if dark else '#0d0d2b'};
}}

/* ── Textarea ── */
.stTextArea textarea {{
    background: {'rgba(6,6,20,0.8)' if dark else 'rgba(248,248,255,0.9)'} !important;
    color: {'#e8e8ff' if dark else '#0d0d2b'} !important;
    border: 1px solid {'rgba(99,102,241,0.2)' if dark else 'rgba(99,102,241,0.18)'} !important;
    border-radius: 14px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    transition: all 0.3s !important;
    padding: 14px !important;
}}
.stTextArea textarea:focus {{
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1), 0 0 20px rgba(99,102,241,0.08) !important;
    outline: none !important;
}}
.stTextArea textarea::placeholder {{
    color: {'#3a3a6a' if dark else '#b0b0d0'} !important;
}}

/* ── Main Review button ── */
.stButton > button {{
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%) !important;
    background-size: 200% 200% !important;
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.4s ease !important;
    position: relative !important;
    overflow: hidden !important;
}}
.stButton > button:hover {{
    background-position: right center !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.4) !important;
}}
.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* ── Radio ── */
.stRadio > div {{
    background: {'rgba(99,102,241,0.06)' if dark else 'rgba(99,102,241,0.04)'};
    border: 1px solid {'rgba(99,102,241,0.15)' if dark else 'rgba(99,102,241,0.12)'};
    border-radius: 12px;
    padding: 8px 12px;
    gap: 16px !important;
}}
.stRadio label {{ color: {'#e8e8ff' if dark else '#0d0d2b'} !important; font-size: 13px !important; }}

/* ── File uploader ── */
div[data-testid="stFileUploader"] {{
    background: {'rgba(99,102,241,0.05)' if dark else 'rgba(99,102,241,0.03)'} !important;
    border: 2px dashed {'rgba(99,102,241,0.3)' if dark else 'rgba(99,102,241,0.25)'} !important;
    border-radius: 14px !important;
    padding: 16px !important;
    transition: all 0.3s !important;
}}
div[data-testid="stFileUploader"]:hover {{
    border-color: rgba(99,102,241,0.5) !important;
    background: {'rgba(99,102,241,0.08)' if dark else 'rgba(99,102,241,0.06)'} !important;
}}

/* ── Review output ── */
.review-output {{
    background: {'rgba(6,6,20,0.7)' if dark else 'rgba(248,248,255,0.9)'};
    border: 1px solid {'rgba(99,102,241,0.2)' if dark else 'rgba(99,102,241,0.15)'};
    border-left: 3px solid #6366f1;
    border-radius: 14px;
    padding: 1.4rem;
    font-size: 13.5px;
    line-height: 1.9;
    color: {'#e8e8ff' if dark else '#0d0d2b'};
    font-family: 'Space Grotesk', sans-serif;
    white-space: pre-wrap;
    max-height: 480px;
    overflow-y: auto;
}}
.review-output::-webkit-scrollbar {{ width: 4px; }}
.review-output::-webkit-scrollbar-track {{ background: transparent; }}
.review-output::-webkit-scrollbar-thumb {{ background: rgba(99,102,241,0.4); border-radius: 4px; }}

/* ── Empty state ── */
.empty-state {{
    background: {'rgba(99,102,241,0.04)' if dark else 'rgba(99,102,241,0.03)'};
    border: 2px dashed {'rgba(99,102,241,0.15)' if dark else 'rgba(99,102,241,0.12)'};
    border-radius: 16px;
    padding: 3.5rem 2rem;
    text-align: center;
}}
.empty-icon {{
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
    animation: float 4s ease-in-out infinite;
}}
@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
}}
.empty-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {'#e8e8ff' if dark else '#0d0d2b'};
    margin-bottom: 0.4rem;
}}
.empty-sub {{
    font-size: 0.8rem;
    color: {'#6b6b9a' if dark else '#9090c0'};
    font-family: 'Fira Code', monospace;
}}

/* ── Code stats pill ── */
.code-stats {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: {'rgba(99,102,241,0.08)' if dark else 'rgba(99,102,241,0.06)'};
    border: 1px solid {'rgba(99,102,241,0.18)' if dark else 'rgba(99,102,241,0.14)'};
    border-radius: 8px;
    padding: 5px 12px;
    font-family: 'Fira Code', monospace;
    font-size: 0.72rem;
    color: {'#8888cc' if dark else '#6666aa'};
    margin-top: 6px;
}}
.code-stats span {{ color: #6366f1; font-weight: 500; }}

/* ── Alerts ── */
.stAlert {{ border-radius: 12px !important; }}
.stSuccess {{ border-left: 3px solid #10b981 !important; }}
.stInfo {{ border-left: 3px solid #6366f1 !important; }}
.stWarning {{ border-left: 3px solid #f59e0b !important; }}

/* ── Download button ── */
.stDownloadButton > button {{
    background: {'rgba(99,102,241,0.1)' if dark else 'rgba(99,102,241,0.08)'} !important;
    color: {'#a5b4fc' if dark else '#4f46e5'} !important;
    -webkit-text-fill-color: {'#a5b4fc' if dark else '#4f46e5'} !important;
    border: 1px solid {'rgba(99,102,241,0.25)' if dark else 'rgba(99,102,241,0.2)'} !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.3s !important;
}}
.stDownloadButton > button:hover {{
    background: {'rgba(99,102,241,0.18)' if dark else 'rgba(99,102,241,0.14)'} !important;
    transform: translateY(-1px) !important;
}}

/* ── Divider ── */
hr {{ border-color: {'rgba(99,102,241,0.15)' if dark else 'rgba(99,102,241,0.12)'} !important; }}

/* ── Selectbox ── */
.stSelectbox > div > div {{
    background: {'rgba(6,6,20,0.8)' if dark else 'rgba(248,248,255,0.9)'} !important;
    border-color: {'rgba(99,102,241,0.2)' if dark else 'rgba(99,102,241,0.18)'} !important;
    border-radius: 10px !important;
    color: {'#e8e8ff' if dark else '#0d0d2b'} !important;
}}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: #6366f1 !important; }}

/* ── Caption ── */
.stCaption {{ color: {'#6b6b9a' if dark else '#9090c0'} !important; font-family: 'Fira Code', monospace !important; font-size: 0.72rem !important; }}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-logo">⚡</span>
        <div class="sidebar-title">AI Code Reviewer</div>
        <div class="sidebar-sub">groq · langchain · rag · faiss</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Theme toggle
    theme_label = "☀️  Light Mode" if dark else "🌙  Dark Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()

    # Stats
    st.markdown("**📊 Session Stats**")
    rag_ok = "✅" if st.session_state.vectorstore else "○"
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <span class="stat-val">{st.session_state.review_count}</span>
            <span class="stat-lbl">Reviews</span>
        </div>
        <div class="stat-card">
            <span class="stat-val">{rag_ok}</span>
            <span class="stat-lbl">RAG</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # RAG Upload
    st.markdown("**📚 Custom Guidelines**")
    st.caption("Upload PDF coding standards for personalized review")
    uploaded_docs = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if uploaded_docs:
        if st.button("⚡ Build Knowledge Base", use_container_width=True):
            with st.spinner("Processing documents..."):
                st.session_state.vectorstore = create_vectorstore(uploaded_docs)
            st.success("✅ RAG ready!")

    st.divider()

    # Tech stack
    st.markdown("**🛠 Tech Stack**")
    techs = ["Groq LPU", "Llama 3 70B", "LangChain", "FAISS", "HuggingFace", "Streamlit"]
    badges = "".join([f'<span class="tech-badge">{t}</span>' for t in techs])
    st.markdown(f'<div class="badge-wrap">{badges}</div>', unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">⚡ powered by groq · llama 3 70b</div>
    <div class="hero-title">AI Code Reviewer</div>
    <div class="hero-desc">bug detection · security audit · performance · pep8 · refactored code</div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── MAIN COLUMNS ──
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <div class="panel-icon">📝</div>
            <div class="panel-title">Your Code</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    input_method = st.radio(
        "Input",
        ["✏️  Paste Code", "📁  Upload .py File"],
        horizontal=True,
        label_visibility="collapsed"
    )

    user_code = ""

    if input_method == "✏️  Paste Code":
        user_code = st.text_area(
            "Code",
            height=360,
            placeholder="# Paste your Python code here...\n\ndef my_function():\n    pass",
            label_visibility="collapsed"
        )
    else:
        uploaded_code = st.file_uploader(
            "Upload .py",
            type=["py"],
            label_visibility="collapsed"
        )
        if uploaded_code:
            user_code = uploaded_code.read().decode("utf-8")
            st.code(user_code, language="python")

    if user_code.strip():
        lines = len(user_code.strip().split("\n"))
        st.markdown(f"""
        <div class="code-stats">
            <span>{lines}</span> lines &nbsp;·&nbsp; <span>{len(user_code)}</span> chars
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  Review My Code", use_container_width=True):
        if user_code.strip():
            with st.spinner("Analyzing with Groq + LangChain..."):
                context = get_relevant_context(st.session_state.vectorstore, user_code)
                review = review_code(user_code, context)
                st.session_state.review = review
                st.session_state.used_rag = bool(context)
                st.session_state.review_count += 1
        else:
            st.warning("⚠️ Please enter some code first!")

with col2:
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-header">
            <div class="panel-icon">📊</div>
            <div class="panel-title">Review Results</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.review:
        if st.session_state.get("used_rag"):
            st.success("✅ Enhanced with your uploaded guidelines (RAG)")
        else:
            st.info("💡 Using general best practices — upload PDF for personalized review")

        st.markdown(
            f'<div class="review-output">{st.session_state.review}</div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾  Download Review",
            data=st.session_state.review,
            file_name="code_review.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-icon">⚡</span>
            <div class="empty-title">Ready to review your code</div>
            <div class="empty-sub">paste code → click review → get instant feedback</div>
        </div>
        """, unsafe_allow_html=True)