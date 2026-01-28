from src.skill_taxonomy import SKILL_WEIGHTS

def calculate_scores(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0
    
    total_weight = 0
    earned_weight = 0
    
    for skill in jd_skills:
        weight = SKILL_WEIGHTS.get(skill, 1.0)
        total_weight += weight
        if skill in resume_skills:
            earned_weight += weight
            
    final_score = (earned_weight / total_weight) * 100
    return round(final_score, 2)