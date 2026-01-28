SkillGap Analyzer — Resume Skill Gap Decision Support System

📄 Overview  
SkillGap Analyzer is a web-based Decision Support System (DSS) that evaluates how well a candidate’s resume aligns with a given job description. The system identifies matched skills, missing skills, and additional skills, calculates a weighted match score, and provides an explainable decision with actionable recommendations.

The application supports both PDF and text-based resumes and is designed to be modular, extensible, and transparent in its decision-making process.

---

📊 Problem Statement  
Resume screening is often time-consuming and subjective. Candidates frequently apply for roles without clear visibility into required skills, while recruiters must manually evaluate large volumes of resumes.

This project aims to automate resume–job matching using rule-based logic while maintaining full explainability of results.

---

🧠 Solution Description  
The system functions as a Decision Support System by:

• Accepting a resume (PDF or pasted text) and a job description  
• Cleaning and normalizing textual input  
• Extracting skills using a predefined taxonomy  
• Comparing resume skills with job requirements  
• Applying weighted scoring logic  
• Producing a decision with justification and recommendations  

The approach avoids black-box machine learning models and focuses on transparent, rule-driven evaluation.

---

🏗 System Architecture  

User Input (Resume + Job Description)  
↓  
Text Preprocessing  
↓  
Skill Extraction (Taxonomy-Based)  
↓  
Skill Matching  
↓  
Weighted Scoring Engine  
↓  
Decision Engine  
↓  
Explainable Output and Recommendations  

---

✨ Key Features  
• PDF and text resume input support  
• Rule-based, explainable decision logic  
• Weighted skill scoring  
• Clear categorization of matched, missing, and extra skills  
• Learning roadmap for identified skill gaps  
• Modular backend design for easy extension  

---

🛠 Technology Stack  

• Programming Language: Python  
• Frontend Framework: Streamlit  
• PDF Processing: pypdf  
• System Type: Rule-Based Decision Support System  
• Deployment: Streamlit Community Cloud  
• Version Control: GitHub  

---

📁 Project Structure  

resume-skill-gap-analyzer/  
│  
├── app/  
│   └── app.py  
│  
├── src/  
│   ├── preprocess.py  
│   ├── skill_taxonomy.py  
│   ├── skill_extraction.py  
│   ├── skill_matching.py  
│   ├── scoring_engine.py  
│   └── decision_engine.py  
│  
├── tests/  
│   └── test_matching.py  
│  
├── requirements.txt  
├── README.md  
└── .gitignore  

---

⚙ Installation and Local Execution  

1. Clone the repository  

git clone https://github.com/<your-username>/resume-skill-gap-analyzer.git  
cd resume-skill-gap-analyzer  

2. Install dependencies  

pip install -r requirements.txt  

3. Run the application  

streamlit run app/app.py  

---

🧪 Testing  

Basic tests are included to validate:  
• Skill matching accuracy  
• Weighted scoring logic  
• Decision classification  

Run tests using:  

python tests/test_matching.py  

---

📈 Example Output  

• Match Score: 62%  
• Decision: Partial Match  
• Matched Skills: Python, Django, REST API  
• Missing Skills: AWS, Docker, PostgreSQL  
• Recommendation: Focus on backend and DevOps skill enhancement  

---

🔄 Version History  

v1.0 — Core Decision Support System with technical skill matching  
v1.1 — PDF resume upload and UI enhancements  
v2.0 (Planned) — Support for non-technical domains and multi-role analysis  

---

🌱 Future Enhancements  

• Non-technical skill domain support  
• Skill synonym normalization  
• Category-wise scoring breakdown  
• Multi-job comparison support  
• Domain detection (Technical / Non-Technical)  

---

👤 Author  

Priyanka Kumari  
Computer Science Student  
GitHub: https://github.com/Priyanka-2509  

---

📜 License  

This project is intended for educational and portfolio purposes.
