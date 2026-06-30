import os

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def test_gemini():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello in one sentence."
    )

    return response.text


def analyze_github_profile(profile, statistics, top_repositories):

    prompt = f"""
You are a friendly AI career coach for students.

Your job is to help students improve their GitHub profile step by step so they become recruiter-ready.

IMPORTANT RULES:
- Keep responses SHORT and EASY to understand.
- Avoid long paragraphs.
- Do NOT sound like a strict interviewer.
- Do NOT assume unknown data.
- Focus only on improvement guidance.
- Use simple English suitable for college students.

---

STUDENT GITHUB DATA

Profile:
Name: {profile.get("name")}
Username: {profile.get("username")}
Bio: {profile.get("bio")}

Statistics:
Total Repositories: {statistics.get("total_repositories")}
Total Stars: {statistics.get("total_stars")}
Total Forks: {statistics.get("total_forks")}
Most Used Language: {statistics.get("most_used_language")}

Top Repositories:
{top_repositories}

---

TASK

Evaluate the GitHub profile and return:

1. GitHub Score (0-100)
   - Base it ONLY on:
     • number of repositories
     • consistency (if available)
     • diversity of languages
     • presence of projects
     • activity level (updated_at if available)
   - Do NOT guess private data
   - Keep scoring simple and explainable

2. Profile Level (Beginner / Improving / Good / Strong)

3. What is GOOD (max 3 points)

4. What needs IMPROVEMENT (max 3 points)

5. Quick Fixes (actionable steps student can do in 1–2 days)

6. Project Ideas (max 3 simple ideas based on current skill level)

---

OUTPUT FORMAT RULES:
- VERY SHORT bullet points
- No long explanations
- Student-friendly tone
- Avoid paragraphs
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text