# api/llm_loader.py
from langchain_community.llms import Ollama


def load_llm():
    return Ollama(
        model="llama3.2",
        temperature=0.0,
        system="""
You are an expert recruiter and hiring assistant.

- Analyze the content carefully.
- Reason through it step-by-step.
- Return only valid JSON.
- Do not add explanations, commentary, or markdown.
- Ensure JSON keys are double-quoted and syntax is correct.

Be consistent and follow the structure precisely.
"""
    )
