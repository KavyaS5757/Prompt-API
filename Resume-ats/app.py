from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import json
import re
import pdfplumber
from groq import Groq

# ── Groq client ──────────────────────────────────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"  # Currently supported model


# ── PDF text extraction ───────────────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file) -> str:
    """Extract plain text from every page of the uploaded PDF."""
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")
    uploaded_file.seek(0)
    with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages).strip()


def extract_text_from_pdf_file(file_path: str) -> str:
    """Extract plain text from a PDF file by path."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with pdfplumber.open(file_path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages).strip()


# ── Generic Groq call ─────────────────────────────────────────────────────────
def call_groq(system_prompt: str, user_content: str, max_tokens: int = 2048) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ══════════════════════════════════════════════════════════════════════════════
#  FEATURE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def feature_resume_review(resume_text: str, jd_text: str) -> str:
    system = (
        "You are an experienced Technical Human Resource Manager. "
        "Review the resume against the job description and give a professional evaluation. "
        "Highlight strengths and weaknesses in relation to the job requirements."
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user)


def feature_ats_score(resume_text: str, jd_text: str) -> str:
    system = (
        "You are a skilled ATS (Applicant Tracking System) scanner. "
        "Evaluate the resume against the job description. "
        "Output format:\n"
        "1. Match Percentage: X%\n"
        "2. Keywords Missing: (list)\n"
        "3. Final Thoughts: (paragraph)"
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user)


def feature_keyword_gap(resume_text: str, jd_text: str) -> str:
    system = (
        "You are an ATS keyword specialist. "
        "Compare the resume to the job description and identify:\n"
        "- Hard skills missing\n"
        "- Soft skills missing\n"
        "- Tools / technologies missing\n"
        "- Certifications or qualifications missing\n"
        "Be specific and actionable. Format each section as a bullet list."
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user)


def feature_rewrite_suggestions(resume_text: str, jd_text: str) -> str:
    system = (
        "You are a professional resume coach. "
        "Given the resume and the job description, identify 3–5 weak or missing bullet points "
        "and rewrite them to be stronger, more ATS-friendly, and tailored to the JD. "
        "Use the STAR/CAR format where applicable. "
        "Show the original (if exists) and the improved version side by side."
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user, max_tokens=3000)


def feature_section_scores(resume_text: str, jd_text: str) -> dict:
    system = (
        "You are an ATS scoring engine. Score the resume against the job description "
        "on each section from 0–100. Return ONLY valid JSON with this exact schema:\n"
        '{"skills": <int>, "experience": <int>, "education": <int>, '
        '"certifications": <int>, "overall": <int>, "summary": "<one sentence>"}'
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    raw = call_groq(system, user, max_tokens=512)
    # strip markdown fences if present
    raw = re.sub(r"```[a-z]*", "", raw).replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": raw}


def feature_cover_letter(resume_text: str, jd_text: str, candidate_name: str) -> str:
    system = (
        "You are an expert cover letter writer. "
        "Write a professional, concise (3–4 paragraphs) cover letter tailored to the job description, "
        "based on the candidate's resume. Address it to 'Hiring Manager'. "
        f"The candidate's name is {candidate_name or 'the applicant'}."
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user, max_tokens=1500)


def feature_multi_job(resume_text: str, jd_list: list[str]) -> str:
    formatted = "\n\n".join(
        [f"--- JD {i+1} ---\n{jd}" for i, jd in enumerate(jd_list)]
    )
    system = (
        "You are an ATS scoring engine. Compare the single resume against multiple job descriptions. "
        "For each JD output:\n"
        "- JD title / label\n"
        "- Match score (0–100)\n"
        "- Top 3 matching strengths\n"
        "- Top 2 gaps\n"
        "Finish with a ranked summary of which JD is the best fit and why."
    )
    user = f"Resume:\n{resume_text}\n\nJob Descriptions:\n{formatted}"
    return call_groq(system, user, max_tokens=3000)


def feature_ats_format_check(resume_text: str) -> str:
    system = (
        "You are an ATS compatibility checker. "
        "Analyse the resume text for common ATS-unfriendly issues such as:\n"
        "- Missing standard sections (Contact, Summary, Experience, Education, Skills)\n"
        "- Use of tables or columns (hard to parse)\n"
        "- Inconsistent date formats\n"
        "- Acronyms without full forms\n"
        "- Vague language or buzzwords without evidence\n"
        "List each issue found and give a specific fix. If no issues, say so."
    )
    return call_groq(system, resume_text)


def feature_recruiter_simulation(resume_text: str, jd_text: str, role: str) -> str:
    system = (
        f"You are a senior recruiter specialising in {role or 'this field'}. "
        "Review the resume as you would during a real screening call. "
        "Give honest, blunt feedback on:\n"
        "1. First impression (would you call this candidate?)\n"
        "2. Red flags\n"
        "3. Questions you would ask in the interview\n"
        "4. Your recommendation: Strong Yes / Yes / Maybe / No"
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user)


def feature_interview_prep(resume_text: str, jd_text: str) -> str:
    system = (
        "You are an interview coach. Based on the resume and the job description, generate:\n"
        "1. 5 behavioural questions likely to be asked\n"
        "2. 5 technical / role-specific questions\n"
        "3. 2 tricky or stress-test questions\n"
        "For each question include a brief tip on what a great answer should cover."
    )
    user = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"
    return call_groq(system, user, max_tokens=3000)


# ══════════════════════════════════════════════════════════════════════════════
#  STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")
st.title("📄 ATS Resume Expert")
st.caption("Powered by Groq · LLaMA 3 70B")

# ── Sidebar – feature selector ────────────────────────────────────────────────
with st.sidebar:
    st.header("🛠️ Choose Features")
    st.markdown("Select which analyses you want to run:")

    feat_review    = st.checkbox("📋 Resume Review",            value=True)
    feat_score     = st.checkbox("📊 ATS Score & Keywords",     value=True)
    feat_gap       = st.checkbox("🔍 Keyword Gap Analysis",     value=False)
    feat_rewrite   = st.checkbox("✏️ Rewrite Suggestions",      value=False)
    feat_sections  = st.checkbox("📈 Section-wise Scoring",     value=False)
    feat_cover     = st.checkbox("📝 Cover Letter Generator",   value=False)
    feat_multi     = st.checkbox("🏆 Multi-Job Comparison",     value=False)
    feat_format    = st.checkbox("⚙️ ATS Format Check",         value=False)
    feat_recruiter = st.checkbox("🎭 Recruiter Simulation",     value=False)
    feat_interview = st.checkbox("🎤 Interview Prep Questions", value=False)

    st.divider()
    st.markdown("**Model:** `llama-3.3-70b-versatile`")
    st.markdown("Set `GROQ_API_KEY` in your `.env` file.")

# ── Main inputs ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**📄 Resume Input** (Choose one method):")
    input_method = st.radio(
        "How do you want to provide your resume?",
        options=["Upload PDF", "File Path", "Paste Text"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    resume_text = ""
    
    if input_method == "Upload PDF":
        uploaded_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
        if uploaded_file:
            st.success("✅ PDF uploaded successfully")
    
    elif input_method == "File Path":
        file_path = st.text_input(
            "📁 Enter full path to PDF file",
            placeholder="e.g. C:\\Users\\YourName\\resume.pdf"
        )
        if file_path:
            st.info("✓ File path entered (will process when you click Analyse)")
    
    else:  # Paste Text
        resume_text = st.text_area(
            "📝 Paste resume text",
            height=250,
            placeholder="Paste your resume content here…"
        )
        if resume_text:
            st.success(f"✓ {len(resume_text.split())} words pasted")

with col2:
    jd_text = st.text_area("📋 Job Description", height=300,
                            placeholder="Paste the job description here…")

# Extra inputs shown only when their feature is selected
candidate_name = ""
role_label = ""
multi_jds: list[str] = []

if feat_cover:
    candidate_name = st.text_input("Your name (for cover letter)", placeholder="e.g. Priya Sharma")

if feat_recruiter:
    role_label = st.text_input("Role / industry (for recruiter persona)",
                                placeholder="e.g. Data Engineer at a fintech startup")

if feat_multi:
    st.markdown("**Paste up to 5 additional job descriptions** (one per box):")
    for i in range(1, 6):
        jd_extra = st.text_area(f"Job Description {i+1}", height=120,
                                 key=f"jd_extra_{i}",
                                 placeholder=f"Paste JD #{i+1} here (leave blank to skip)…")
        if jd_extra.strip():
            multi_jds.append(jd_extra.strip())

st.divider()

# ── Run button ────────────────────────────────────────────────────────────────
run = st.button("🚀 Analyse Resume", type="primary", use_container_width=True)

if run:
    # ── Validation ─────────────────────────────────────────────────────────
    if input_method == "Upload PDF" and not uploaded_file:
        st.error("Please upload a resume PDF.")
        st.stop()
    elif input_method == "File Path" and not file_path:
        st.error("Please enter the file path.")
        st.stop()
    elif input_method == "Paste Text" and not resume_text.strip():
        st.error("Please paste your resume text.")
        st.stop()

    any_feature = any([feat_review, feat_score, feat_gap, feat_rewrite,
                       feat_sections, feat_cover, feat_multi, feat_format,
                       feat_recruiter, feat_interview])
    if not any_feature:
        st.warning("Please select at least one feature from the sidebar.")
        st.stop()

    needs_jd = any([feat_review, feat_score, feat_gap, feat_rewrite,
                    feat_sections, feat_cover, feat_recruiter, feat_interview])
    if needs_jd and not jd_text.strip():
        st.error("Please paste a job description for the selected features.")
        st.stop()

    # ── Extract resume text ────────────────────────────────────────────────
    if input_method != "Paste Text":
        with st.spinner("Extracting text from PDF…"):
            try:
                if input_method == "Upload PDF":
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif input_method == "File Path":
                    resume_text = extract_text_from_pdf_file(file_path)
            except Exception as e:
                st.error(f"Could not read PDF: {e}")
                st.stop()

    if not resume_text:
        st.error("Could not extract text from the PDF. Ensure it is not scanned/image-only.")
        st.stop()

    st.success(f"Extracted {len(resume_text.split())} words from resume.")
    st.divider()

    # 1. Resume Review
    if feat_review:
        with st.expander("📋 Resume Review", expanded=True):
            with st.spinner("Analysing resume…"):
                st.markdown(feature_resume_review(resume_text, jd_text))

    # 2. ATS Score
    if feat_score:
        with st.expander("📊 ATS Score & Keyword Match", expanded=True):
            with st.spinner("Scoring resume…"):
                st.markdown(feature_ats_score(resume_text, jd_text))

    # 3. Keyword Gap
    if feat_gap:
        with st.expander("🔍 Keyword Gap Analysis", expanded=True):
            with st.spinner("Finding keyword gaps…"):
                st.markdown(feature_keyword_gap(resume_text, jd_text))

    # 4. Rewrite Suggestions
    if feat_rewrite:
        with st.expander("✏️ Rewrite Suggestions", expanded=True):
            with st.spinner("Generating rewrites…"):
                st.markdown(feature_rewrite_suggestions(resume_text, jd_text))

    # 5. Section-wise Scores
    if feat_sections:
        with st.expander("📈 Section-wise Scoring", expanded=True):
            with st.spinner("Scoring each section…"):
                scores = feature_section_scores(resume_text, jd_text)
                if "error" in scores:
                    st.warning(f"Could not parse JSON scores:\n{scores['error']}")
                else:
                    cols = st.columns(5)
                    labels = ["Skills", "Experience", "Education", "Certifications", "Overall"]
                    keys   = ["skills", "experience", "education", "certifications", "overall"]
                    for col, label, key in zip(cols, labels, keys):
                        with col:
                            val = scores.get(key, 0)
                            color = "#2ecc71" if val >= 70 else "#e67e22" if val >= 45 else "#e74c3c"
                            st.markdown(
                                f"<div style='text-align:center'>"
                                f"<p style='font-size:13px;margin-bottom:4px'>{label}</p>"
                                f"<p style='font-size:34px;font-weight:700;color:{color};margin:0'>{val}</p>"
                                f"<p style='font-size:11px;color:gray'>/100</p></div>",
                                unsafe_allow_html=True,
                            )
                    st.progress(scores.get("overall", 0) / 100)
                    st.info(scores.get("summary", ""))

    # 6. Cover Letter
    if feat_cover:
        with st.expander("📝 Cover Letter", expanded=True):
            with st.spinner("Writing cover letter…"):
                letter = feature_cover_letter(resume_text, jd_text, candidate_name)
                st.markdown(letter)
                st.download_button("⬇️ Download Cover Letter",
                                   data=letter,
                                   file_name="cover_letter.txt",
                                   mime="text/plain")

    # 7. Multi-Job Comparison
    if feat_multi:
        with st.expander("🏆 Multi-Job Comparison", expanded=True):
            all_jds = ([jd_text] if jd_text.strip() else []) + multi_jds
            if len(all_jds) < 2:
                st.warning("Add at least 2 job descriptions (main + extras) for comparison.")
            else:
                with st.spinner(f"Comparing against {len(all_jds)} JDs…"):
                    st.markdown(feature_multi_job(resume_text, all_jds))

    # 8. ATS Format Check
    if feat_format:
        with st.expander("⚙️ ATS Format Check", expanded=True):
            with st.spinner("Checking ATS compatibility…"):
                st.markdown(feature_ats_format_check(resume_text))

    # 9. Recruiter Simulation
    if feat_recruiter:
        with st.expander("🎭 Recruiter Simulation", expanded=True):
            with st.spinner("Simulating recruiter perspective…"):
                st.markdown(feature_recruiter_simulation(resume_text, jd_text, role_label))

    # 10. Interview Prep
    if feat_interview:
        with st.expander("🎤 Interview Prep Questions", expanded=True):
            with st.spinner("Generating interview questions…"):
                st.markdown(feature_interview_prep(resume_text, jd_text))

    st.divider()
    st.success("✅ Analysis complete!")