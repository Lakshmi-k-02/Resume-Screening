import re

def analyze_resume(text):
    """
    Extract skills and experience from resume text
    """
    # Example simple skill list
    known_skills = ["Python", "SQL", "Data Analysis", "Machine Learning", "Excel", "Tableau"]
    
    # Find skills in resume text (case-insensitive)
    skills_found = [skill for skill in known_skills if re.search(r'\b' + skill + r'\b', text, re.I)]

    # Extract experience in years (simple regex for numbers followed by 'year' or 'years')
    exp_match = re.search(r'(\d+)\s+year', text, re.I)
    experience = exp_match.group(1) + " years" if exp_match else "Unknown"

    # Dummy name (could use NLP later)
    name = "Candidate"

    return {
        "name": name,
        "skills": skills_found,
        "experience": experience
    }
