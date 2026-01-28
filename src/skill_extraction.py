import re
from src.skill_taxonomy import SKILL_TAXONOMY

def extract_skills(text):
    found_skills = set()
    for category, skill_list in SKILL_TAXONOMY.items():
        for skill in skill_list:
            # \b ensures we match 'java' but not 'javascript' when looking for 'java'
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, text):
                found_skills.add(skill)
    return found_skills