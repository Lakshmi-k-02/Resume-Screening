Resume Screening Agent 
📌 Overview

This Resume Screening Agent analyzes a candidate’s resume against a job description.
It extracts text from PDF resumes, processes the job description, and evaluates the candidate using AI.
The system returns match percentage, candidate status, missing skills, and feedback.

✨ Features

Upload PDF resume and text-based job description

Automatic text extraction from PDFs

AI-powered candidate evaluation

Provides:
✔ Skill match percentage
✔ Shortlisting decision
✔ Detailed feedback

Simple UI built using Streamlit

⚠️ Limitations

Works best with text-based PDFs (not scanned images)

Requires a valid API key to run AI evaluation

Internet is needed if using cloud AI models

🛠 Tech Stack & APIs Used
Backend

FastAPI

PyPDF2 (PDF text extraction)

Frontend (UI)

Streamlit

AI / LLM

OpenAI API 

🚀 Setup & Run Instructions
1️⃣ Install required libraries
pip install -r requirements.txt

2️⃣ Install Uvicorn (server)
pip install uvicorn

3️⃣ Start the Backend API

Navigate to the project folder:

uvicorn app.main:app --reload

4️⃣ Start the Streamlit UI

Open a second terminal → go to the ui folder:

cd ui
streamlit run app.py

5️⃣ Use the Application

Upload resume (PDF)

Upload job description (text)

Get skill match % and evaluation result

🔧 Potential Improvements

Add OCR to support scanned PDF resumes

Improve evaluation using custom datasets

Add multilingual resume support

Add export options (PDF/Excel report)

Add security and user authentication

Build a database to store past evaluations
