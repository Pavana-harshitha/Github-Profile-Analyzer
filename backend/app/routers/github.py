from fastapi import APIRouter
from app.services.github_service import get_profile, get_repositories
from app.services.github_service import get_profile
from app.services.gemini_service import analyze_github_profile

router = APIRouter()


#@router.get("/{username}")
#def get_github_profile(username: str):
#    return get_profile(username)

#@router.get("/{username}/repos")
#def github_repositories(username: str):
#    return get_repositories(username)

#@router.get("/gemini/test")
#def gemini_test():
#    return {
#        "response": test_gemini()
#    }


@router.get("/{username}/analyze")
def analyze(username: str):

    profile = get_profile(username)

    repository_data = get_repositories(username)

    ai_analysis = analyze_github_profile(
        profile,
        repository_data["statistics"],
        repository_data["top_repositories"]
    )
    print(ai_analysis)
    return {
        "profile": profile,
        "statistics": repository_data["statistics"],
        "language_distribution": repository_data["language_distribution"],
        "top_repositories": repository_data["top_repositories"],
        "ai_analysis": ai_analysis
    }