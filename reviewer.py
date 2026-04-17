from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_model():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )

def review_code(code: str, context: str = "") -> str:
    model = get_model()

    rag_section = f"""
Relevant documentation/guidelines context:
{context}
Use the above context to give more accurate review.
""" if context else ""

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Python code reviewer with 10+ years of experience.
You review code for:
1. Bugs and errors
2. Security vulnerabilities
3. Performance issues
4. Code quality and best practices
5. Suggestions for improvement

Be specific, clear and constructive. Format your response with clear sections."""),
        ("human", f"""{rag_section}
Please review the following Python code:

```python
{{code}}
```

Provide:
- Overall assessment
- Bugs/Errors found
- Security issues
- Performance suggestions
- Code quality feedback
- Improved version of the code
""")
    ])

    chain = prompt | model
    result = chain.invoke({"code": code})
    return result.content