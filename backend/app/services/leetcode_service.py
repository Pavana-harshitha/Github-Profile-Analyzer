import requests
from app.services.gemini_service import client


BASE_URL = "https://leetcode-api-faisalshohag.vercel.app"


def fetch_leetcode_profile(username: str):
    try:
        res = requests.get(f"{BASE_URL}/{username}", timeout=10)

        if res.status_code != 200:
            return {"error": "LeetCode API failed"}

        data = res.json()

        return {
            "username": username,
            "total_solved": data.get("totalSolved") or 0,
            "easy": data.get("easySolved") or 0,
            "medium": data.get("mediumSolved") or 0,
            "hard": data.get("hardSolved") or 0,
            "ranking": data.get("ranking") or "N/A",
            "contest_rating": data.get("contestRating") or "N/A"
        }

    except Exception as e:
        return {"error": str(e)}
    


def analyze_leetcode_profile(data: dict):

    prompt = f"""
You are a senior DSA mentor and career coach.

Analyze this LeetCode profile.

IMPORTANT RULES:
- Be honest but encouraging
- Do NOT assume missing data
- Keep output structured and concise
- Focus on improvement roadmap

---

LEETCODE DATA:
- Total Solved: {data.get("total_solved") or 0}
- Easy: {data.get("easy") or 0}
- Medium: {data.get("medium") or 0}
- Hard: {data.get("hard") or 0}
- Ranking: {data.get("ranking")}
- Contest Rating: {data.get("contest_rating")}

---

TASK:

Return:

1. Coding Profile Score (0–100)
2. Skill Level (Beginner / Intermediate / Advanced)
3. Strengths (max 3 bullets)
4. Weaknesses (max 3 bullets)
5. Strong Topics
6. Weak Topics
7. Suggested Topics to Study Next
8. Contest Improvement Plan
9. Weekly Practice Plan

Keep it simple and student-friendly.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text