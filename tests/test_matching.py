import sys
import os

# Allow tests to access src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.skill_matching import perform_matching
from src.scoring_engine import calculate_scores
from src.decision_engine import make_decision

def test_skill_matching():
    resume_skills = {"python", "sql", "docker"}
    jd_skills = {"python", "java", "docker"}

    result = perform_matching(resume_skills, jd_skills)

    assert result["matched"] == {"python", "docker"}
    assert result["missing"] == {"java"}
    assert result["extra"] == {"sql"}

    print("✔ Skill matching test passed")


def test_scoring_engine():
    resume_skills = {"python", "docker"}
    jd_skills = {"python", "java", "docker"}

    score = calculate_scores(resume_skills, jd_skills)

    # python(2.0) + docker(1.5) earned = 3.5
    # python(2.0) + java(2.0) + docker(1.5) total = 5.5
    expected_score = (3.5 / 5.5) * 100

    assert abs(score - expected_score) < 0.01

    print("✔ Scoring engine test passed")


def test_decision_engine():
    decision_strong = make_decision(80, set())
    decision_partial = make_decision(55, {"java", "aws"})
    decision_low = make_decision(20, {"java", "aws", "docker"})

    assert decision_strong["label"] == "Strong Match"
    assert decision_partial["label"] == "Partial Match"
    assert decision_low["label"] == "Low Match"

    print("✔ Decision engine test passed")


if __name__ == "__main__":
    test_skill_matching()
    test_scoring_engine()
    test_decision_engine()

    print("\nAll tests passed successfully.")
