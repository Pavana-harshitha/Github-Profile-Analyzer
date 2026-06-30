import pdfplumber
from app.services.gemini_service import client


def extract_text_from_pdf(file) -> str:
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def analyze_linkedin_pdf(file):

    text = extract_text_from_pdf(file)

    if not text.strip():
        return "Could not extract text from PDF. Please upload a clear LinkedIn PDF."

    prompt = f"""
You are a friendly AI career coach helping students improve their LinkedIn profile.

IMPORTANT:
- Keep output short and student-friendly
- Do NOT assume missing information
- Focus only on LinkedIn content

---

LINKEDIN PROFILE CONTENT:
{text}

---

TASK:

Return:

1. LinkedIn Score (0-100)
Calculate based on following criteria
Scoring Criteria:

    1. Professional Headline (10)
    - Clear and professional
    - Mentions role or specialization

    2. Summary/About (15)
    - Explains interests, skills and goals

    3. Experience (25)
    - Internship or work experience
    - Relevant responsibilities

    4. Education (15)
    - Degree
    - College
    - Graduation year

    5. Skills (10)
    - Technical skills listed

    6. Certifications (10)
    - Relevant certifications

    7. Contact Information (5)
    - Email and LinkedIn profile available

    8. Overall Professionalism & Completeness (10)
    - Well-structured
    - Few missing sections
    - Suitable for recruiters


2. Profile Summary (2-3 lines)
3. Strengths (max 3)
4. Weaknesses (max 3)
5. Missing Improvements
6. Quick Fixes
7. Job Readiness Level


"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text