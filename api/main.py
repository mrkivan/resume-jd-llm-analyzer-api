import asyncio
import time
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import json

from api.utils.file_loader import load_document
from api.utils.llm_loader import load_llm
from api.prompts.prompt_resume_jd import job_description_parser_prompt, resume_parser_prompt
from api.prompts.prompt_evaluation import match_evaluation_prompt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resume Match API")

# Asynchronous file saving with logging
async def save_file(upload_file: UploadFile, file_path: str):
    start_time = time.time()
    with open(file_path, "wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)
    end_time = time.time()
    logger.info(f"File saved: {upload_file.filename} in {end_time - start_time:.2f} seconds")

# Extract structured data (with better prompts for quality)

def extract_fields(text, role, llm):
    start_time = time.time()
    if role== "resume":
        result = llm(resume_parser_prompt(text)).strip()
    else:
        result = llm(job_description_parser_prompt(text)).strip()
    end_time = time.time()
    logger.info(f"Extracted fields for {role} in {end_time - start_time:.2f} seconds")
    return result

# Evaluate how well resume matches the job description
def evaluate_match(resume_info, jd_info, llm):
    start_time = time.time()
    result = llm(match_evaluation_prompt(resume_info, jd_info)).strip()
    end_time = time.time()
    logger.info(f"Evaluated match in {end_time - start_time:.2f} seconds")
    return result

def safe_parse_json(raw_text, label):
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse {label} as JSON",
            "raw_text": raw_text.strip(),
            "exception": str(e)
        }

# Main API endpoint
@app.post("/match", summary="Evaluate Resume vs Job Description")
async def match_resume_and_jd(
        resume: UploadFile = File(..., description="Upload resume PDF"),
        job: UploadFile = File(..., description="Upload job description PDF or TXT")
):
    start_time = time.time()

    resume_path = f"temp_{resume.filename}"
    job_path = f"temp_{job.filename}"

    # Save uploaded files asynchronously
    await asyncio.gather(
        save_file(resume, resume_path),
        save_file(job, job_path)
    )

    # Track time for processing and logging
    try:
        llm = load_llm()

        logger.info("🔄 Loading documents...")
        # Load both resume and job description concurrently
        resume_text, jd_text = await asyncio.gather(
            asyncio.to_thread(load_document, resume_path),
            asyncio.to_thread(load_document, job_path)
        )

        logger.info("🧠 Extracting resume and job description information...")
        # Extract structured info concurrently
        resume_info, jd_info = await asyncio.gather(
            asyncio.to_thread(extract_fields, resume_text, "resume", llm),
            asyncio.to_thread(extract_fields, jd_text, "job description", llm)
        )

        logger.info("🔍 Evaluating match...")
        # Evaluate match
        evaluation = evaluate_match(resume_info, jd_info, llm)

        end_time = time.time()
        logger.info(f"Total time taken for API call: {end_time - start_time:.2f} seconds")

        return JSONResponse({
            "resume_info": safe_parse_json(resume_info, "resume_info"),
            "job_description_info": safe_parse_json(jd_info, "job_description_info"),
            "evaluation": safe_parse_json(evaluation, "evaluation")
        })
    finally:
        os.remove(resume_path)
        os.remove(job_path)
