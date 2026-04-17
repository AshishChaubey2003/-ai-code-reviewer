from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agent_state import CodeReviewState
import re

def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)


# ── NODE 1: Bug Analyzer ──────────────────────────────────────────────────────
def analyze_bugs_node(state: CodeReviewState) -> dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Python bug detector. Be precise and concise."),
        ("human", """Analyze this Python code for bugs and logical errors.

{rag_section}

Code:
```python
{code}
```

List each bug on a new line starting with '- '.
If no bugs found, write 'NO_BUGS'.
Also give a bug severity score from 0 (no bugs) to 10 (critical bugs).
Format: SCORE: <number>
""")
    ])

    rag_section = f"Guidelines context:\n{state['rag_context']}" if state['rag_context'] else ""
    result = llm.invoke(prompt.format_messages(
        code=state['fixed_code'] or state['code'],
        rag_section=rag_section
    ))

    content = result.content
    bugs = []
    score = 5

    if "NO_BUGS" not in content:
        bugs = [line.strip() for line in content.split('\n') if line.strip().startswith('- ')]

    score_match = re.search(r'SCORE:\s*(\d+)', content)
    if score_match:
        score = min(10, int(score_match.group(1)))

    return {
        **state,
        "bugs": bugs,
        "bug_score": score,
        "review_steps": state['review_steps'] + ["Bug Analysis"]
    }


# ── NODE 2: Auto-Fix (runs only when bugs found) ──────────────────────────────
def auto_fix_node(state: CodeReviewState) -> dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Python developer. Fix bugs without changing working logic."),
        ("human", """Fix the following bugs in this Python code.

Bugs found:
{bugs}

Code to fix:
```python
{code}
```

Return ONLY the fixed Python code, no explanation, no markdown fences.
""")
    ])

    result = llm.invoke(prompt.format_messages(
        code=state['fixed_code'] or state['code'],
        bugs="\n".join(state['bugs'])
    ))

    fixed = result.content.strip()
    # strip markdown fences if LLM adds them anyway
    fixed = re.sub(r'^```python\n?', '', fixed)
    fixed = re.sub(r'\n?```$', '', fixed)

    return {
        **state,
        "fixed_code": fixed,
        "fix_attempts": state['fix_attempts'] + 1,
        "review_steps": state['review_steps'] + [f"Auto-Fix (attempt {state['fix_attempts'] + 1})"]
    }


# ── NODE 3: Security Auditor ──────────────────────────────────────────────────
def security_node(state: CodeReviewState) -> dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Python security expert. Check for OWASP Top 10 and common vulnerabilities."),
        ("human", """Audit this Python code for security vulnerabilities.

Code:
```python
{code}
```

Check for:
- SQL injection
- Hardcoded secrets/API keys
- Unsafe eval/exec usage
- Path traversal
- Insecure deserialization
- Any OWASP Top 10 issues

List each issue starting with '- '.
If none found, write 'NO_ISSUES'.
Security score from 0 (critical issues) to 10 (secure): SCORE: <number>
""")
    ])

    code_to_check = state['fixed_code'] or state['code']
    result = llm.invoke(prompt.format_messages(code=code_to_check))
    content = result.content

    issues = []
    score = 8

    if "NO_ISSUES" not in content:
        issues = [line.strip() for line in content.split('\n') if line.strip().startswith('- ')]

    score_match = re.search(r'SCORE:\s*(\d+)', content)
    if score_match:
        score = min(10, int(score_match.group(1)))

    return {
        **state,
        "security_issues": issues,
        "security_score": score,
        "review_steps": state['review_steps'] + ["Security Audit"]
    }


# ── NODE 4: Performance + Quality Reviewer ───────────────────────────────────
def quality_node(state: CodeReviewState) -> dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Python performance and code quality expert."),
        ("human", """Review this Python code for performance and quality.

{rag_section}

Code:
```python
{code}
```

Check for:
- Performance bottlenecks (unnecessary loops, missing caching)
- PEP8 violations
- Poor naming conventions
- Missing error handling
- Code duplication

List issues starting with '- '.
Quality score 0-10: SCORE: <number>
""")
    ])

    rag_section = f"Guidelines:\n{state['rag_context']}" if state['rag_context'] else ""
    code_to_check = state['fixed_code'] or state['code']

    result = llm.invoke(prompt.format_messages(
        code=code_to_check,
        rag_section=rag_section
    ))
    content = result.content

    issues = [line.strip() for line in content.split('\n') if line.strip().startswith('- ')]
    score = 7
    score_match = re.search(r'SCORE:\s*(\d+)', content)
    if score_match:
        score = min(10, int(score_match.group(1)))

    return {
        **state,
        "performance_issues": issues,
        "quality_score": score,
        "review_steps": state['review_steps'] + ["Quality & Performance Review"]
    }


# ── NODE 5: Report Generator ──────────────────────────────────────────────────
def report_node(state: CodeReviewState) -> dict:
    overall = round((state['bug_score'] + state['security_score'] + state['quality_score']) / 3, 1)

    bugs_section = "\n".join(state['bugs']) if state['bugs'] else "No bugs found."
    security_section = "\n".join(state['security_issues']) if state['security_issues'] else "No security issues found."
    perf_section = "\n".join(state['performance_issues']) if state['performance_issues'] else "No performance issues found."
    fix_section = f"```python\n{state['fixed_code']}\n```" if state['fixed_code'] else "No fixes required."

    report = f"""## AI Code Review Report
**Agent Steps:** {' → '.join(state['review_steps'])}
**Fix Attempts:** {state['fix_attempts']}

---

### Scores
| Category | Score |
|---|---|
| Bug Severity | {state['bug_score']}/10 |
| Security | {state['security_score']}/10 |
| Code Quality | {state['quality_score']}/10 |
| **Overall** | **{overall}/10** |

---

### Bugs Found ({len(state['bugs'])})
{bugs_section}

---

### Security Issues ({len(state['security_issues'])})
{security_section}

---

### Performance & Quality ({len(state['performance_issues'])} issues)
{perf_section}

---

### Auto-Fixed Code
{fix_section}
"""

    return {
        **state,
        "final_report": report,
        "review_steps": state['review_steps'] + ["Report Generated"]
    }