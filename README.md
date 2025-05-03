# Resume-JD LLM Based Analyzer API

A FastAPI-based backend that intelligently matches resumes with job descriptions using an LLM (e.g., LLaMA via Ollama). It extracts structured data from both documents and evaluates the resume's fit, generating a match score and summary.

## 🔍 Features

- Upload resume and job description (PDF/TXT)
- Extract structured info (skills, tools, experience, certifications)
- Evaluate fit using an LLM
- Returns a match score, summary, and missing skills
- Modular architecture (prompt-engineering, document loading, etc.)

## 🧠 LLM Capabilities

- Model: `llama3.2` (via [Ollama](https://ollama.com/))
- Controlled with system prompts and deterministic output using `temperature=0.0`

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Ollama installed with `llama3.2` model pulled

### Setup

```bash
git clone https://github.com/your-username/resume-jd-llm-analyzer-api.git
cd resume-jd-llm-analyzer-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
