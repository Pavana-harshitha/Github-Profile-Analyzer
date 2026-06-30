from fastapi import APIRouter
from app.services.leetcode_service import fetch_leetcode_profile,analyze_leetcode_profile

router = APIRouter()


@router.get("/{username}/analyze")
def analyze(username: str):

    profile = fetch_leetcode_profile(username)

    if "error" in profile:
        return profile

    analysis = analyze_leetcode_profile(profile)
    print(analysis)

    return {
        "profile": profile,
        "analysis": analysis
    }