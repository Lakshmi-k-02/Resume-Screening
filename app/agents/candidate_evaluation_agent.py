def evaluate_candidate(candidate_details, jd_details):
    """
    Compare candidate skills to JD skills
    """
    candidate_skills = set([s.lower() for s in candidate_details.get("skills", [])])
    jd_skills = set([s.lower() for s in jd_details.get("skills_required", [])])

    if not jd_skills:
        match_percentage = 0
        matched_skills = []
        missing_skills = []
    else:
        matched_skills = list(candidate_skills.intersection(jd_skills))
        missing_skills = list(jd_skills - candidate_skills)
        match_percentage = int(len(matched_skills) / len(jd_skills) * 100)

    status = "Selected" if match_percentage >= 50 else "Rejected"
    feedback = f"{match_percentage}% of required skills matched."

    return {
        "status": status,
        "feedback": feedback,
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
