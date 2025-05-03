# For resume & JD extraction
# api/prompt_resume_jd.py

# Extract structured data (with better prompts for quality)

def job_description_parser_prompt(text: str) -> str:
    return f"""
    You are an intelligent parser. Extract structured data from the given job description.
    
- "general_info": job title, company name.
- "key_skills": Give the Array of the software, programming languages, and tools mentioned.
- "technologies_and_tools": Give the Array of the mentioned technologies.
- "years_of_experience": Explicitly mention the number of years if stated.
- "certifications": Give the Array of certifications.

Guidelines:
- Return only **valid JSON**. No comments, markdown, or extra text.
- Use lowercase snake_case keys.
- Do not fabricate information. If a field is missing, return an empty list or null.
- Be precise and consistent with formatting.

Job Description Text:
{text}
"""

def resume_parser_prompt(resume_text: str) -> str:
    return f"""
You are a professional resume parser trained to extract structured data from candidate resumes.

Your task is to extract and return the following fields as valid JSON:
- "general_info": name, contact details,
- "key_skills": A list of technical or domain-specific skills (e.g., Python, AWS, Machine Learning)
- "technologies_and_tools": A list of tools, platforms, or frameworks mentioned (e.g., Docker, TensorFlow, Git)
- "years_of_experience": The total number of years of professional experience (as a number). Estimate only if clearly implied.
- "certifications": A list of certifications mentioned (e.g., PMP, AWS Certified Solutions Architect)

Guidelines:
- Return only **valid JSON**. No comments, markdown, or extra text.
- Use lowercase snake_case keys.
- Do not fabricate information. If a field is missing, return an empty list or null.
- Be precise and consistent with formatting.

Resume Text:
\"\"\"
{resume_text}
\"\"\"
"""


