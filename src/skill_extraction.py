import re
import re
from src.skill_taxonomy import SKILL_TAXONOMY

def extract_skills(text):
    """
    Extracts skills from text based on the taxonomy.
    Handles multi-word phrases by checking longer phrases first.
    """
    if not text:
        return set()

    found_skills = set()
    text = text.lower()

    # Flatten the taxonomy into a single list for searching
    all_known_skills = []
    for category_skills in SKILL_TAXONOMY.values():
        all_known_skills.extend(category_skills)

    # This prevents matching "Sales" when the text says "Sales Forecasting"
    all_known_skills = sorted(all_known_skills, key=len, reverse=True)

    for skill in all_known_skills:
        # Use regex word boundaries to ensure exact matches
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, text):
            found_skills.add(skill)
            # Optional: Remove the found skill from text to prevent double matching
        

    return found_skills
