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
    return round(final_score, 2)from src.skill_taxonomy import SKILL_WEIGHTS, SKILL_TAXONOMY

def calculate_scores(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0, {}

    # 1. Overall Weighted Score
    total_weight = 0
    earned_weight = 0
    for skill in jd_skills:
        weight = SKILL_WEIGHTS.get(skill, 1.0)
        total_weight += weight
        if skill in resume_skills:
            earned_weight += weight
    
    overall_score = round((earned_weight / total_weight) * 100, 2)

    # 2. Category-wise Breakdown
    cat_breakdown = {}
    for category, skills in SKILL_TAXONOMY.items():
        # What skills from this category are required in the JD?
        relevant_in_jd = [s for s in skills if s in jd_skills]
        if relevant_in_jd:
            # How many of those does the candidate have?
            matched = [s for s in relevant_in_jd if s in resume_skills]
            cat_breakdown[category] = len(matched) / len(relevant_in_jd)

    return overall_score, cat_breakdown
