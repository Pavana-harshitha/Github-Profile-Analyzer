from fastapi import APIRouter
from app.services.github_service import get_profile
router = APIRouter()


@router.get("/{username}")
def get_github_profile(username: str):
    return get_profile(username)