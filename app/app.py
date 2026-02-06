import streamlit as st
import sys
import os
from pypdf import PdfReader
import plotly.graph_objects as go

# Link to src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocess import clean_text
from src.skill_extraction import extract_skills
from src.skill_matching import perform_matching
from src.scoring_engine import calculate_scores
from src.decision_engine import make_decision


# PDF EXTRACTION
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


# PROFESSIONAL LIGHT THEME CSS
def local_css():
    st.markdown("""
        <style>
        /* Main background and text */
        .stApp { background-color: #F8FAFC; color: #1E293B; }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0; }

        /* Card styling */
        .stats-card {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Hero Header Score */
        .hero-section {
            background-color: #FFFFFF;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #E2E8F0;
            text-align: center;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        /* Professional Tags */
        .tag {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 8px;
            font-weight: 500;
            margin: 5px;
            font-size: 13px;
        }
        .tag-match { background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
        .tag-miss { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
        .tag-extra { background-color: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }

        /* Course Link Buttons */
        .course-btn {
            display: block;
            text-decoration: none;
            background-color: #FFFFFF;
            color: #2563EB;
            padding: 14px;
            border-radius: 10px;
            border: 1px solid #DBEAFE;
            margin-bottom: 12px;
            font-weight: 600;
            text-align: center;
            transition: all 0.2s;
        }
        .course-btn:hover {
            background-color: #2563EB;
            color: #FFFFFF;
            border-color: #2563EB;
        }
        </style>
    """, unsafe_allow_html=True)

# PAGE CONFIG
st.set_page_config(page_title="DSS Analyzer", layout="wide", page_icon="📐")
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
    analyze_btn = st.button("🚀 GENERATE REPORT", use_container_width=True, type="primary")

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
        st.error("No recognizable skills found in the Job Description.")
        st.stop()

    matches = perform_matching(res_skills, jd_skills)
    score, cat_scores = calculate_scores(res_skills, jd_skills)
    decision = make_decision(score, matches["missing"])

    # HEADER SECTION
    st.markdown(f"""
        <div class="hero-section">
            <p style="color: #64748B; font-weight: 600; text-transform: uppercase; margin-bottom: 5px;">Overall Compatibility</p>
            <h1 style="color: #1E293B; font-size: 72px; margin: 0;">{score}%</h1>
            <div style="margin-top: 15px;">
                <span style="background-color: {decision['color']}; color: white; padding: 8px 25px; border-radius: 50px; font-weight: bold; font-size: 18px;">
                    {decision['label']}
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    #  Graphs & Analysis
    with col1:
        # Radar Chart for Industry Strength
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.subheader("🕸 Industry Competency Radar")
        
        categories = list(cat_scores.keys())
        values = [v * 100 for v in cat_scores.values()]
        
        # Plotly Radar logic
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line_color='#2563EB',
            fillcolor='rgba(37, 99, 235, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20),
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.subheader("📢 Decision Analysis")
        st.write(f"**Justification:** {decision['explanation']}")
        st.write(f"**Recommended Action:** {decision['recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)

    #  Skills & Roadmap
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.subheader("🔍 Skill Inventory")
        
        st.write("**Matched Strengths:**")
        if matches["matched"]:
            match_html = "".join([f'<span class="tag tag-match">{s.title()}</span>' for s in sorted(matches["matched"])])
            st.markdown(match_html, unsafe_allow_html=True)
        else: st.write("No direct matches.")

        st.write("---")
        st.write("**Critical Gaps:**")
        if matches["missing"]:
            miss_html = "".join([f'<span class="tag tag-miss">{s.title()}</span>' for s in sorted(matches["missing"])])
            st.markdown(miss_html, unsafe_allow_html=True)
        else: st.write("Perfect match! No gaps.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.subheader("💡 Learning Roadmap")
        if matches["missing"]:
            st.write("Click to master missing competencies:")
            for s in list(matches["missing"])[:3]:
                st.markdown(f"""
                    <a href="https://www.coursera.org/search?query={s}" target="_blank" class="course-btn">
                        📘 Master {s.title()} Certification →
                    </a>
                """, unsafe_allow_html=True)
        else:
            st.success("Candidate is fully qualified for this role.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.subheader("📁 Bonus Skills")
        if matches["extra"]:
            st.write("Candidate also offers:")
            bonus_html = "".join([f'<span class="tag tag-extra">{s.title()}</span>' for s in sorted(matches["extra"])])
            st.markdown(bonus_html, unsafe_allow_html=True)
        else:
            st.write("No additional industry skills detected.")
        st.markdown('</div>', unsafe_allow_html=True)

# LANDING VIEW
else:
    st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <h1 style="color: #1E293B; font-size: 50px;">📐 Universal SkillGap Analyzer</h1>
            <p style="color: #64748B; font-size: 20px; max-width: 700px; margin: 0 auto;">
                A professional Decision Support System to evaluate candidate alignment across Tech, Business, Travel, and Finance domains.
            </p>
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 50px;">
                <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid #E2E8F0; width: 220px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="margin: 0;">📊</h2><h4 style="margin: 10px 0;">Weighted Scoring</h4>
                </div>
                <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid #E2E8F0; width: 220px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="margin: 0;">🕸</h2><h4 style="margin: 10px 0;">Radar Visualization</h4>
                </div>
                <div style="background: white; padding: 25px; border-radius: 12px; border: 1px solid #E2E8F0; width: 220px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="margin: 0;">📚</h2><h4 style="margin: 10px 0;">Upskilling Links</h4>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
