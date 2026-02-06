import streamlit as st
import sys
import os
from pypdf import PdfReader
import plotly.graph_objects as go
import plotly.express as px

# Link to src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocess import clean_text
from src.skill_extraction import extract_skills
from src.skill_matching import perform_matching
from src.scoring_engine import calculate_scores
from src.decision_engine import make_decision

# --- PDF EXTRACTION ---
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except:
        return ""

# --- DARK DASHBOARD CSS ---
def local_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #ffffff; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }

        /* Card Container */
        .res-card {
            background-color: #1c2128;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #30363d;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }

        /* Hero Header */
        .hero-section {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            border: 1px solid #3b82f6;
        }

        /* Skill Tags */
        .tag {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            margin: 4px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .tag-match { background-color: #064e3b; color: #10b981; border-color: #059669; }
        .tag-miss { background-color: #450a0a; color: #f87171; border-color: #b91c1c; }
        .tag-extra { background-color: #1e3a8a; color: #60a5fa; border-color: #2563eb; }

        /* Course Buttons */
        .course-link {
            display: block;
            background-color: #2d333b;
            color: #58a6ff !important;
            padding: 12px;
            border-radius: 8px;
            text-decoration: none;
            margin-bottom: 8px;
            border: 1px solid #444c56;
            transition: 0.3s;
        }
        .course-link:hover { background-color: #3b82f6; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# --- APP CONFIG ---
st.set_page_config(page_title="SkillGap DSS Dashboard", layout="wide", page_icon="📐")
local_css()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📐 Analyzer Pro")
    st.markdown("---")
    input_method = st.radio("Resume Format", ["📄 Upload PDF/TXT", "✍️ Paste Text"])
    
    resume_text = ""
    if "Upload" in input_method:
        up = st.file_uploader("Upload File", type=["pdf", "txt"])
        if up:
            resume_text = extract_text_from_pdf(up) if up.type == "application/pdf" else up.read().decode()
    else:
        resume_text = st.text_area("Paste Resume Content", height=200)

    jd_text = st.text_area("Paste Job Description", height=200)
    st.markdown("---")
    analyze_btn = st.button("🚀 EXECUTE ANALYSIS", use_container_width=True, type="primary")

# --- DASHBOARD LOGIC ---
if analyze_btn and resume_text and jd_text:
    # 1. Pipeline
    rc, jc = clean_text(resume_text), clean_text(jd_text)
    rs, js = extract_skills(rc), extract_skills(jc)
    
    if not js:
        st.error("No industry keywords detected in Job Description.")
        st.stop()
        
    matches = perform_matching(rs, js)
    score, cat_scores = calculate_scores(rs, js)
    decision = make_decision(score, matches["missing"])

    # 2. Hero Section
    st.markdown(f"""
        <div class="hero-section">
            <h1 style="margin:0; font-size: 60px;">{score}%</h1>
            <p style="font-size: 20px; opacity: 0.8;">Hiring Verdict: <b style="color:{decision['color']}">{decision['label']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Dashboard Grid
    col_a, col_b = st.columns([1, 1], gap="medium")

    with col_a:
        # GRAPH 1: Category Proficiency (Horizontal Bar)
        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("📁 Competency by Category")
        
        categories = list(cat_scores.keys())
        values = [v * 100 for v in cat_scores.values()]
        
        fig_bar = px.bar(
            x=values, y=categories, orientation='h',
            labels={'x': 'Proficiency (%)', 'y': ''},
            template="plotly_dark", color=values,
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(height=300, margin=dict(l=0, r=0, t=20, b=0), coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Analysis Summary Card
        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("📢 DSS Summary")
        st.write(f"**Justification:** {decision['explanation']}")
        st.write(f"**Strategic Recommendation:** {decision['recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        # GRAPH 2: Skill Distribution (Donut Chart)
        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("📊 Skill Set Composition")
        
        labels = ['Matched', 'Missing']
        values = [len(matches['matched']), len(matches['missing'])]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=.6,
            marker_colors=['#10b981', '#ef4444']
        )])
        fig_pie.update_layout(template="plotly_dark", height=300, margin=dict(l=0, r=0, t=20, b=0), showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Persona Generation Logic
        persona = "Generalist"
        if cat_scores.get("Technology", 0) > 0.7: persona = "Technical Specialist"
        elif cat_scores.get("Soft Skills", 0) > 0.8: persona = "Leadership Driven"
        elif cat_scores.get("Travel & Tourism", 0) > 0.6: persona = "Hospitality Expert"

        st.markdown('<div class="res-card">', unsafe_allow_html=True)
        st.subheader("👤 Candidate Persona")
        st.info(f"The system identifies this candidate as a: **{persona}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Detailed Skill Inventory (Full Width)
    st.markdown("---")
    st.subheader("🔍 Detailed Skill Audit")
    t1, t2, t3 = st.tabs(["✅ Matched", "❌ Missing", "⭐ Bonus Skills"])
    
    with t1:
        if matches['matched']:
            html = "".join([f'<span class="tag tag-match">{s.title()}</span>' for s in matches['matched']])
            st.markdown(html, unsafe_allow_html=True)
        else: st.write("No matches found.")

    with t2:
        if matches['missing']:
            html = "".join([f'<span class="tag tag-miss">{s.title()}</span>' for s in matches['missing']])
            st.markdown(html, unsafe_allow_html=True)
            st.markdown("### 🎓 Recommended Upskilling")
            for s in list(matches['missing'])[:3]:
                st.markdown(f'<a href="https://www.coursera.org/search?query={s}" class="course-link">Master {s.title()} on Coursera →</a>', unsafe_allow_html=True)
        else: st.write("Zero gaps identified.")

    with t3:
        if matches['extra']:
            html = "".join([f'<span class="tag tag-extra">{s.title()}</span>' for s in matches['extra']])
            st.markdown(html, unsafe_allow_html=True)
        else: st.write("No additional industry skills detected.")

else:
    # LANDING VIEW
    st.markdown("""
        <div style="text-align: center; padding: 100px 20px;">
            <h1 style="font-size: 50px; color: #3b82f6;">📐 SkillGap Analyzer Pro</h1>
            <p style="font-size: 20px; opacity: 0.7;">An advanced Decision Support System for Industry-Agnostic Talent Acquisition.</p>
            <p style="opacity: 0.5;">Upload a Resume and Job Description to begin the analytical process.</p>
        </div>
    """, unsafe_allow_html=True)
