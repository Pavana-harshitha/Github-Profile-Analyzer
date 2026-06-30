from fastapi import APIRouter
from app.services.github_service import get_profile
from app.services.github_service import get_profile, get_repositories

router = APIRouter()


@router.get("/{username}")
def get_github_profile(username: str):
    return get_profile(username)

@router.get("/{username}/repos")
def github_repositories(username: str):
    return get_repositories(username)