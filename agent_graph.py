from langgraph.graph import StateGraph, END
from agent_state import CodeReviewState
from agent_nodes import (
    analyze_bugs_node,
    auto_fix_node,
    security_node,
    quality_node,
    report_node,
)


# ── Conditional edge: should we fix or move on? ───────────────────────────────
def should_fix_or_continue(state: CodeReviewState) -> str:
    has_bugs = len(state['bugs']) > 0
    under_limit = state['fix_attempts'] < state['max_attempts']

    if has_bugs and under_limit:
        return "fix"        # loop: fix then re-analyze
    return "security"       # no more bugs OR max attempts reached


# ── Build the graph ───────────────────────────────────────────────────────────
def build_review_graph():
    graph = StateGraph(CodeReviewState)

    # Register nodes
    graph.add_node("analyze",  analyze_bugs_node)
    graph.add_node("fix",      auto_fix_node)
    graph.add_node("security", security_node)
    graph.add_node("quality",  quality_node)
    graph.add_node("report",   report_node)

    # Entry point
    graph.set_entry_point("analyze")

    # Conditional edge from analyze — this is the loop
    graph.add_conditional_edges(
        "analyze",
        should_fix_or_continue,
        {
            "fix":      "fix",
            "security": "security",
        }
    )

    # After fix → re-analyze (the loop back)
    graph.add_edge("fix",      "analyze")

    # Linear path after bugs resolved
    graph.add_edge("security", "quality")
    graph.add_edge("quality",  "report")
    graph.add_edge("report",   END)

    return graph.compile()


# ── Public function called by app.py ─────────────────────────────────────────
def run_review_agent(code: str, rag_context: str = "") -> dict:
    app = build_review_graph()

    initial_state: CodeReviewState = {
        "code": code,
        "rag_context": rag_context,
        "bugs": [],
        "security_issues": [],
        "performance_issues": [],
        "fixed_code": "",
        "fix_attempts": 0,
        "max_attempts": 3,      # max retry loop count
        "bug_score": 0,
        "security_score": 10,
        "quality_score": 10,
        "final_report": "",
        "review_steps": [],
    }

    result = app.invoke(initial_state)
    return result