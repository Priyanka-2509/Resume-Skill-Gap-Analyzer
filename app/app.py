import streamlit as st
import sys
import os
from pypdf import PdfReader

# Link to src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocess import clean_text
from src.skill_extraction import extract_skills
from src.skill_matching import perform_matching
from src.scoring_engine import calculate_scores
from src.decision_engine import make_decision


# PDF EXTRACTION (SAFE)
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


# CUSTOM CSS (THEMING)
def local_css():
    st.markdown("""
        <style>
        .main { background-color: #0e1117; color: #ffffff; }

        .res-card {
            background-color: #1f2937;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #374151;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        .match-tag {
            background-color: #064e3b;
            color: #10b981;
            padding: 4px 12px;
            border-radius: 20px;
            margin: 4px;
            display: inline-block;
            border: 1px solid #10b981;
            font-size: 14px;
        }

        .miss-tag {
            background-color: #450a0a;
            color: #f87171;
            padding: 4px 12px;
            border-radius: 20px;
            margin: 4px;
            display: inline-block;
            border: 1px solid #f87171;
            font-size: 14px;
        }

        .hero-score {
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            border-radius: 20px;
            margin-bottom: 30px;
        }
        
        .cat-label {
            font-size: 14px;
            font-weight: bold;
            color: #94a3b8;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

# PAGE CONFIG
st.set_page_config(page_title="SkillGap DSS", layout="wide", page_icon="📐")
local_css()


# SIDEBAR
with st.sidebar:
    st.title("⚙️ Analysis Panel")
    st.markdown("---")

    resume_method = st.radio("Resume Input", ["📄 Upload PDF/TXT", "✍️ Paste Text"])
    resume_text = ""

    if "Upload" in resume_method:
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
    else:
        resume_text = st.text_area("Paste Resume Content", height=200)

    jd_text = st.text_area("Paste Job Description", height=200)

    st.markdown("---")
    analyze_btn = st.button(" RUN ANALYTICS", use_container_width=True)

# MAIN UI
if analyze_btn:
    if not resume_text or not jd_text:
        st.error("Missing input data!")
        st.stop()

    # PIPELINE 
    res_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    res_skills = extract_skills(res_clean)
    jd_skills = extract_skills(jd_clean)

    if not jd_skills:
        st.error("No recognizable skills found in the Job Description. Please ensure it contains relevant industry keywords.")
        st.stop()

    matches = perform_matching(res_skills, jd_skills)
    
    # Updated: scoring_engine now returns (score, category_breakdown)
    score, cat_scores = calculate_scores(res_skills, jd_skills)
    
    decision = make_decision(score, matches["missing"])

    
    # HERO SECTION
    st.markdown(f"""
        <div class="hero-score">
            <h1 style='margin:0; font-size: 50px;'>{score}% Match</h1>
            <p style='font-size: 20px; opacity: 0.9;'>System Decision: <b>{decision['label']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    # LEFT COLUMN
    with col1:
        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("📢 Decision Analysis")
        st.write(f"**Justification:** {decision['explanation']}")
        st.write(f"**Recommended Action:** {decision['recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("📊 Skill Gaps")

        st.write("**Identified Strengths:**")
        if matches["matched"]:
            # Sort skills alphabetically for better display
            match_html = "".join(
                [f'<span class="match-tag">{s.title()}</span>' for s in sorted(matches["matched"])]
            )
            st.markdown(match_html, unsafe_allow_html=True)
        else:
            st.write("No matches.")

        st.write("---")
        st.write("**Missing Requirements:**")
        if matches["missing"]:
            miss_html = "".join(
                [f'<span class="miss-tag">{s.title()}</span>' for s in sorted(matches["missing"])]
            )
            st.markdown(miss_html, unsafe_allow_html=True)
        else:
            st.write("No gaps found!")

        st.markdown('</div>', unsafe_allow_html=True)

    
    # RIGHT COLUMN
    with col2:
        # INDUSTRY STRENGTH SECTION (New for Non-Tech support)
        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("🏢 Industry Strength")
        if cat_scores:
            st.write("Strength based on Job Description requirements:")
            for cat, val in cat_scores.items():
                st.markdown(f'<div class="cat-label">{cat}</div>', unsafe_allow_html=True)
                st.progress(val)
        else:
            st.write("No specific industry categories detected.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("💡 Learning Roadmap")

        if matches["missing"]:
            st.write("To close the gap, prioritize these topics:")
            for s in list(matches["missing"])[:4]:
                st.info(
                    f"📚 **Course search:** "
                    f"[Find {s.title()} resources]"
                    f"(https://www.coursera.org/search?query={s})"
                )
        else:
            st.success("The candidate meets all technical criteria.")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("📁 Bonus Skills")

        if matches["extra"]:
            st.write("Candidate also offers (Not required but valuable):")
            st.write(", ".join([f"**{s.title()}**" for s in matches["extra"]]))
        else:
            st.write("No additional taxonomy skills detected.")

        st.markdown('</div>', unsafe_allow_html=True)

# LANDING VIEW
else:
    st.markdown("""
        <div style="text-align: center; padding: 100px;">
            <h1 style="font-size: 60px;">📐</h1>
            <h2 style="opacity: 0.8;">Universal SkillGap Analyzer</h2>
            <p style="opacity: 0.6;">
                Analyze resumes for <b>Tech, Travel, Business, Marketing, and Finance</b> roles.<br>
                Upload a Resume and Job Description from the sidebar to begin.
            </p>
        </div>
    """, unsafe_allow_html=True)
