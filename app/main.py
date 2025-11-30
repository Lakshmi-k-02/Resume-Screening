import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

from app.parsepdf import parse_pdf
from app.agents.resume_extractor_agent import analyze_resume
from app.agents.jd_extractor_agent import analyze_jd
from app.agents.candidate_evaluation_agent import evaluate_candidate
import json
import io

def extract_from_docx(file_bytes):
    """Extract text from DOCX file"""
    try:
        from docx import Document
        doc = Document(file_bytes)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except ImportError:
        raise Exception("python-docx is required for DOCX support. Install with: pip install python-docx")

app = FastAPI()

from fastapi import FastAPI, UploadFile, Form

@app.post("/screening/")
async def upload_resume(
    resumes: list[UploadFile],
    jd_text: str = Form(...)
):
    """
    Process single or multiple resumes against a job description.
    Supports: PDF, DOCX, DOC, TXT files
    """
    try:
        print(f"Received {len(resumes)} resume file(s)")
        print("Received JD text from Streamlit")

        jd_details = analyze_jd(jd_text)
        results = []

        for resume in resumes:
            try:
                print(f"Processing: {resume.filename}")
                file_bytes = await resume.read()
                
                # Extract text based on file type
                file_ext = resume.filename.lower().split('.')[-1]
                
                if file_ext == 'pdf':
                    resume_file = io.BytesIO(file_bytes)
                    resume_text = parse_pdf(resume_file)
                elif file_ext in ['docx', 'doc']:
                    resume_text = extract_from_docx(io.BytesIO(file_bytes))
                elif file_ext == 'txt':
                    resume_text = file_bytes.decode('utf-8')
                else:
                    results.append({
                        "filename": resume.filename,
                        "error": f"Unsupported file type: {file_ext}. Supported: PDF, DOCX, DOC, TXT"
                    })
                    continue

                candidate_details = analyze_resume(resume_text)
                evaluation = evaluate_candidate(candidate_details, jd_details)

                # Build response for this resume
                result = {
                    "filename": resume.filename,
                    **evaluation,
                    "candidate_details": candidate_details,
                    "jd_details": jd_details
                }
                results.append(result)

            except Exception as e:
                results.append({
                    "filename": resume.filename,
                    "error": str(e)
                })

        return JSONResponse(content={"results": results, "total_processed": len(resumes)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
