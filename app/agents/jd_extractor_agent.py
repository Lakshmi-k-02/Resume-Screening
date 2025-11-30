def analyze_jd(text):
    """
    Extract required skills and experience from job description
    """
    # Split JD text into lines and find known skills (simple example)
    known_skills = ["Python", "SQL", "Data Analysis", "Machine Learning", "Excel", "Tableau"]
    skills_required = [skill for skill in known_skills if skill.lower() in text.lower()]

    # Extract experience (look for '1-3 years', etc.)
    import re
    exp_match = re.search(r'(\d+[-–]\d+)\s+years?', text, re.I)
    experience_required = exp_match.group(1) + " years" if exp_match else "Unknown"

    return {
        "skills_required": skills_required,
        "experience_required": experience_required
    }
