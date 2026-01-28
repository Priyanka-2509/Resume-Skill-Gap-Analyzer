def perform_matching(resume_skills, jd_skills):
    return {
        "matched": resume_skills.intersection(jd_skills),
        "missing": jd_skills - resume_skills,
        "extra": resume_skills - jd_skills
    }