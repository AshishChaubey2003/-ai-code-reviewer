from typing import TypedDict, List, Optional

class CodeReviewState(TypedDict):
    # Input
    code: str
    rag_context: str

    # Analysis results
    bugs: List[str]
    security_issues: List[str]
    performance_issues: List[str]

    # Auto-fix loop
    fixed_code: str
    fix_attempts: int
    max_attempts: int

    # Scores (0-10)
    bug_score: int
    security_score: int
    quality_score: int

    # Final output
    final_report: str
    review_steps: List[str]   # tracks which nodes ran — shown in UI