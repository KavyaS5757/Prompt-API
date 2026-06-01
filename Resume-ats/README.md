# 📄 ATS Resume Expert

A comprehensive Streamlit-based application powered by **Groq's LLaMA 3.3 70B** model that provides intelligent resume analysis, ATS optimization, and job matching capabilities. This tool helps job seekers optimize their resumes for Applicant Tracking Systems and improve their chances of landing interviews.

---

## 🎯 Overview

**ATS Resume Expert** is an all-in-one resume analysis platform that uses advanced AI to:
- Evaluate resumes against job descriptions
- Identify keyword gaps and ATS compatibility issues
- Generate personalized cover letters
- Simulate recruiter screening
- Prepare for interviews
- Compare resumes across multiple job opportunities

The application uses **Groq's fast inference API** with the **LLaMA 3.3 70B** model for quick, high-quality AI analysis.

---

## ✨ Features

### 1. **📋 Resume Review** (Default: ON)
**Purpose:** Professional evaluation of your resume against a job description

**What It Does:**
- Acts as an experienced HR manager reviewing your resume
- Compares your background against job requirements
- Highlights your strengths in relation to the job
- Identifies weaknesses and areas for improvement
- Provides actionable feedback

**Use Case:** Get an expert perspective on how well your resume aligns with the role before submitting an application.

---

### 2. **📊 ATS Score & Keywords** (Default: ON)
**Purpose:** Scan your resume like an Applicant Tracking System

**What It Does:**
- Calculates a match percentage (0-100%)
- Lists missing keywords from the job description
- Provides final thoughts on ATS compatibility
- Identifies critical keywords you should include

**Output Format:**
```
1. Match Percentage: X%
2. Keywords Missing: [list of keywords]
3. Final Thoughts: [paragraph summary]
```

**Use Case:** Understand how likely your resume is to pass through automated ATS systems.

---

### 3. **🔍 Keyword Gap Analysis**
**Purpose:** Deep-dive analysis of skill and keyword mismatches

**What It Does:**
- Identifies **hard skills** missing from your resume (e.g., Python, SQL, AWS)
- Identifies **soft skills** gaps (e.g., communication, leadership)
- Lists missing **tools/technologies** required for the role
- Highlights missing **certifications/qualifications**
- Provides specific, actionable recommendations

**Use Case:** Create a targeted upskilling plan or update your resume with critical keywords.

---

### 4. **✏️ Rewrite Suggestions**
**Purpose:** Get professional resume improvements with examples

**What It Does:**
- Identifies 3-5 weak or missing bullet points in your resume
- Rewrites them to be ATS-friendly and stronger
- Uses **STAR/CAR format** for better impact:
  - **S**ituation, **T**ask, **A**ction, **R**esult
  - **C**hallenge, **A**ction, **R**esult
- Shows original vs. improved version side-by-side
- Aligns suggestions with the job description

**Example:**
```
❌ BEFORE: Managed projects using various tools
✅ AFTER: Led 15+ cross-functional projects with 95% on-time delivery using Agile and Jira
```

**Use Case:** Strengthen your resume language and make it more impactful.

---

### 5. **📈 Section-wise Scoring**
**Purpose:** Get detailed scores for each resume section

**What It Does:**
- Scores resume sections from 0-100:
  - **Skills**: Relevant technical & soft skills
  - **Experience**: Work history alignment
  - **Education**: Educational background fit
  - **Certifications**: Industry certifications match
  - **Overall**: Combined score
- Provides visual score cards with color coding:
  - 🟢 Green (70+): Strong
  - 🟠 Orange (45-69): Moderate
  - 🔴 Red (<45): Needs improvement
- Generates a one-sentence summary

**Use Case:** Identify which resume sections need the most improvement.

---

### 6. **📝 Cover Letter Generator**
**Purpose:** Generate a professional, personalized cover letter

**What It Does:**
- Requires your name (or uses generic "the applicant")
- Writes a professional 3-4 paragraph cover letter
- Tailored to the job description
- Based on your resume content
- Addresses "Hiring Manager"
- Professional tone and structure

**Includes:**
- Opening paragraph (hook & interest)
- Body paragraphs (why you're a good fit)
- Closing paragraph (call to action)

**Download Option:** Save as `.txt` file for easy editing and sending.

**Use Case:** Quickly generate a high-quality cover letter for each application.

---

### 7. **🏆 Multi-Job Comparison**
**Purpose:** Compare your resume against multiple job opportunities

**What It Does:**
- Accepts your main job description + up to 5 additional job descriptions
- For each job, provides:
  - Match score (0-100)
  - Top 3 matching strengths
  - Top 2 gaps to address
- Ranks all jobs by best fit
- Explains why certain roles are better matches

**Output Example:**
```
--- JD 1: Senior Data Engineer ---
Match Score: 85/100
Top 3 Strengths: Python, SQL, AWS
Top 2 Gaps: Spark, Scala

[Ranked summary of all compared jobs]
```

**Use Case:** Apply strategically by identifying which opportunities are the best fit.

---

### 8. **⚙️ ATS Format Check**
**Purpose:** Ensure your resume is ATS-compatible

**What It Does:**
- Analyzes resume text for common ATS issues:
  - ❌ Missing standard sections (Contact, Summary, Experience, Education, Skills)
  - ❌ Use of tables or columns (hard to parse by ATS)
  - ❌ Inconsistent date formats (May 2021 vs 05/2021)
  - ❌ Acronyms without full forms (AWS without "Amazon Web Services")
  - ❌ Vague language or buzzwords without evidence
- Lists each issue found with specific fixes
- Reports "No issues" if your resume is ATS-friendly

**Common Issues & Fixes:**
| Issue | Example | Fix |
|-------|---------|-----|
| Tables | Multi-column layout | Use bullet points instead |
| Dates | 5/2021 and May 21, 2021 | Use consistent format: May 2021 |
| Acronyms | AWS | Amazon Web Services (AWS) |
| Buzzwords | "Go-getter" | "Drove 25% revenue increase in Q3" |

**Use Case:** Before applying, ensure your resume will be properly parsed by ATS software.

---

### 9. **🎭 Recruiter Simulation**
**Purpose:** Get honest, blunt feedback from a recruiter's perspective

**What It Does:**
- Role is customizable (e.g., "Data Engineer at fintech startup")
- Acts as a senior recruiter reviewing your resume
- Provides brutal honesty on:
  - **First Impression**: Would they call you?
  - **Red Flags**: Concerns or deal-breakers
  - **Interview Questions**: What they'd ask you
  - **Recommendation**: Strong Yes / Yes / Maybe / No

**Use Case:** Understand how real recruiters would perceive your resume and prepare for actual screening calls.

---

### 10. **🎤 Interview Prep Questions**
**Purpose:** Prepare for the interview with likely questions

**What It Does:**
- Generates **5 behavioral questions** likely to be asked
  - Example: "Tell me about a time you overcame a technical challenge"
- Generates **5 technical/role-specific questions**
  - Example: "Explain how you'd optimize a slow SQL query"
- Generates **2 tricky/stress-test questions**
  - Example: "How would you handle conflicting priorities?"
- Includes tips for each question on what great answers should cover

**Output Format:**
```
**BEHAVIORAL QUESTION 1:** "Tell me about a time you..."
✅ TIP: Use STAR format, focus on leadership and problem-solving
```

**Use Case:** Practice answering likely interview questions with expert guidance.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Groq API Key (free at [console.groq.com](https://console.groq.com))
- Required Python packages (see Installation)

### Installation

1. **Clone or navigate to the project folder:**
   ```bash
   cd Resume-ats
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install required packages:**
   ```bash
   pip install streamlit groq pdfplumber python-dotenv
   ```

4. **Set up your `.env` file:**
   Create a `.env` file in the `Resume-ats` folder with:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   Get your free API key from [console.groq.com](https://console.groq.com)

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

---

## 📖 How to Use

### Step 1: Provide Your Resume
Choose one of three methods:

#### Method 1: Upload PDF
- Click **"Upload Resume (PDF)"**
- Select your resume file
- App automatically extracts text

#### Method 2: File Path
- Select **"File Path"** option
- Enter the full path: `C:\Users\YourName\resume.pdf`
- App reads the PDF from your system

#### Method 3: Paste Text
- Select **"Paste Text"** option
- Copy-paste your resume content directly
- No file upload needed

### Step 2: Provide Job Description
- Paste the complete job description in the **"Job Description"** text area
- Copy from job posting, LinkedIn, or anywhere
- Include full requirements for best analysis

### Step 3: Select Features
In the left sidebar, check which analyses you want:
- ✅ Resume Review (recommended: always ON)
- ✅ ATS Score & Keywords (recommended: always ON)
- Optional: Select others based on your needs

### Step 4: (Optional) Add Extra Information

**If using Cover Letter Generator:**
- Enter your name in the "Your name" field
- Used for personalization

**If using Recruiter Simulation:**
- Enter role/industry (e.g., "Data Engineer at fintech startup")
- Adds context to recruiter perspective

**If using Multi-Job Comparison:**
- Paste additional job descriptions (up to 5)
- Each gets scored and compared

### Step 5: Click "Analyse Resume"
- Click the **🚀 Analyse Resume** button
- Wait for analysis to complete
- Results expand as they process

### Step 6: Review Results
- Each analysis appears in expandable sections
- Read recommendations carefully
- Download cover letters if needed
- Use insights to improve resume

---

## 📊 Understanding the Output

### Resume Review Output
```
Strengths:
- Strong technical background in Python and cloud platforms
- Clear progression and leadership experience

Weaknesses:
- Limited mention of specific metrics/achievements
- Education section could highlight more certifications
```

### ATS Score Output
```
1. Match Percentage: 78%
2. Keywords Missing: Docker, Kubernetes, CI/CD, Terraform
3. Final Thoughts: Strong candidate overall. Adding containerization 
   technologies would increase match to 85%+
```

### Section Scores Output
```
Skills: 82/100    ✅
Experience: 75/100 ⚠️
Education: 68/100  ⚠️
Certifications: 55/100 ❌
Overall: 70/100
```

### Cover Letter Output
```
Dear Hiring Manager,

I am writing to express my strong interest in the Senior Data 
Engineer position at [Company]. With 7 years of experience in...

[3-4 professional paragraphs]

Sincerely,
[Your Name]
```

---

## ⚙️ Technical Details

### Model Information
- **Model**: Groq's LLaMA 3.3 70B (Latest - as of June 2026)
- **Provider**: Groq (Ultra-fast inference)
- **Temperature**: 0.3 (Consistent, professional responses)
- **Max Tokens**: Varies by feature (512-3000)

### File Format Support
- **PDF**: Fully supported (text extraction)
- **Text**: Direct text input supported
- **File Paths**: Both Windows and Unix paths supported

### Response Times
- Resume Review: ~5-15 seconds
- ATS Score: ~5-10 seconds
- Cover Letter: ~10-20 seconds
- Multi-Job Comparison: ~20-40 seconds (depends on number of jobs)

---

## 🔧 Troubleshooting

### Error: "GROQ_API_KEY not found"
**Solution:** Make sure your `.env` file is in the `Resume-ats` folder and contains:
```env
GROQ_API_KEY=your_actual_key_here
```

### Error: "File not found" (when using File Path)
**Solution:** 
- Use the complete absolute path (e.g., `C:\Users\YourName\Documents\resume.pdf`)
- Ensure the file actually exists at that location
- Use forward slashes or double backslashes: `C:\\Users\\YourName\\resume.pdf`

### Error: "Could not extract text from PDF"
**Causes & Solutions:**
- PDF is scanned/image-only → Convert to text PDF or paste text directly
- PDF is corrupted → Try another PDF reader to verify
- PDF is encrypted → Decrypt first before uploading

### Response is slow or incomplete
- Groq servers may be experiencing high load
- Try again in a few moments
- Larger resumes may take longer (normal behavior)

### Model shows as "decommissioned"
**Solution:** This shouldn't happen with current version. If it does:
- Check your `.env` file for the correct API key
- Ensure you're using the latest version of the app
- Try restarting the Streamlit app

---

## 📋 Tips & Best Practices

### For Best Results:

1. **Format Your Resume Well**
   - Use standard sections: Contact, Summary, Experience, Education, Skills
   - Avoid complex tables or graphics
   - Use consistent date formats (Month Year)
   - Spell out acronyms at first mention

2. **Use Specific, Quantified Achievements**
   - ❌ "Improved system performance"
   - ✅ "Improved API response time by 40% (2s → 1.2s)"

3. **Match Job Description Keywords**
   - Copy exact keywords from the job posting
   - Use industry-standard terminology
   - Include both hard skills and soft skills

4. **Tailor for Each Role**
   - Don't use a one-size-fits-all resume
   - Reorder skills/experience to highlight most relevant
   - Use the Multi-Job Comparison to find best fit roles

5. **Follow Up on Recommendations**
   - Update your resume based on Gap Analysis
   - Fix ATS Format issues immediately
   - Practice Interview Prep questions

---

## 📝 Feature Comparison Table

| Feature | JD Required | Resume Only | Output Type | Time |
|---------|------------|------------|-------------|------|
| Resume Review | ✅ Yes | No | Text | 5-10s |
| ATS Score | ✅ Yes | No | Text | 5-10s |
| Keyword Gap | ✅ Yes | No | Text | 5-10s |
| Rewrite Suggestions | ✅ Yes | No | Text | 10-15s |
| Section Scores | ✅ Yes | No | JSON/Visual | 5-10s |
| Cover Letter | ✅ Yes | No | Text+Download | 10-20s |
| Multi-Job Comparison | ✅ Yes (Multiple) | No | Text | 20-40s |
| ATS Format Check | ❌ No | ✅ Yes | Text | 5-10s |
| Recruiter Simulation | ✅ Yes | No | Text | 10-15s |
| Interview Prep | ✅ Yes | No | Text | 10-15s |

---

## 🎓 Use Case Examples

### Scenario 1: College Graduate Applying First Time
1. Upload resume
2. Enable: Resume Review, ATS Score, Keyword Gap, Interview Prep
3. Fix gaps and practice questions
4. Re-run to verify improvements

### Scenario 2: Career Changer
1. Enable all features
2. Use Recruiter Simulation to understand how experience translates
3. Use Rewrite Suggestions to reframe existing experience
4. Generate Cover Letter to explain transition

### Scenario 3: Applying to Multiple Roles
1. Use Multi-Job Comparison
2. Identify which roles you're best-suited for
3. Tailor resume specifically for top-match roles
4. Generate personalized Cover Letters for each

### Scenario 4: ATS Optimization
1. Focus on: ATS Score, Keyword Gap, ATS Format Check
2. Fix all identified issues
3. Re-run to verify improvements
4. Check new ATS score

---

## 📞 Support & FAQs

### Q: Is my data private?
**A:** Your resume and job description data is sent to Groq's servers for AI analysis. Groq doesn't store this data long-term. For maximum privacy, review Groq's privacy policy.

### Q: Can I use this for multiple jobs?
**A:** Yes! The Multi-Job Comparison feature is designed exactly for this. Compare up to 6 job opportunities at once.

### Q: How often should I update my resume?
**A:** Run analysis every time you:
- Apply to a new type of role
- Have new accomplishments to add
- Change industries or functions

### Q: Can I edit the generated suggestions in the app?
**A:** The app displays suggestions for copying elsewhere. Copy the text and edit in your resume editor, then upload again to verify.

### Q: What if my resume is very long (10+ pages)?
**A:** The app works with any length, but condensing to 1-2 pages is generally recommended for ATS compatibility.

---

## 🔄 Workflow Suggestions

### Recommended Workflow:

```
1. RUN → ATS Format Check (if first time)
   ↓
2. FIX → Any format issues found
   ↓
3. RUN → Resume Review + ATS Score + Keyword Gap
   ↓
4. IMPROVE → Resume based on recommendations
   ↓
5. RUN → Rewrite Suggestions
   ↓
6. ENHANCE → Bullet points with stronger language
   ↓
7. RUN → Section Scores to verify improvements
   ↓
8. PREPARE → Interview Prep + Cover Letter
   ↓
9. APPLY → With confidence!
```

---

## 📦 Project Structure

```
Resume-ats/
├── app.py                 # Main Streamlit application
├── README.md             # This documentation
├── .env                  # Your Groq API key (create this)
└── (uploads/)           # Temporary folder for uploaded files
```

---

## 🎉 Getting the Most Out of ATS Resume Expert

- Run analysis **before submitting applications**
- Use **multiple features** for comprehensive feedback
- Apply recommendations **iteratively**
- Track **score improvements** over time
- Compare **multiple opportunities** to find best fit
- Practice **interview questions** thoroughly

---

## 📄 Version Information

- **App Version**: 1.0
- **AI Model**: Groq LLaMA 3.3 70B
- **Last Updated**: June 2026
- **Status**: Fully Functional

---

## 🤝 Contributing & Feedback

If you find issues or have suggestions:
1. Test thoroughly
2. Document the issue clearly
3. Note your Streamlit/Python versions
4. Provide sample resume/JD if applicable

---

## 📜 License

This project is provided as-is for educational and professional use.

---

**Good luck with your job applications! 🚀**

