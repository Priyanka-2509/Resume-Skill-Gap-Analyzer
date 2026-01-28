def make_decision(score, missing_skills):
    if score >= 75:
        return {
            "label": "Strong Match",
            "color": "green",
            "explanation": "The candidate is highly qualified for this role with most core skills present.",
            "recommendation": "Proceed to technical interview."
        }
    elif 40 <= score < 75:
        return {
            "label": "Partial Match",
            "color": "orange",
            "explanation": f"The candidate has a good foundation but lacks key skills like: {', '.join(list(missing_skills)[:3])}.",
            "recommendation": "Consider for a junior role or provide upskilling plan."
        }
    else:
        return {
            "label": "Low Match",
            "color": "red",
            "explanation": "The candidate's technical profile does not align with the current requirements.",
            "recommendation": "Keep in database for future roles that fit their specific stack."
        }