from fastapi import FastAPI
from app.routers.github import router as github_router
from app.routers.linkedin import router as linkedin_router
from app.routers.leetcode import router as leetcode_router

app = FastAPI()

app.include_router(
    github_router,
    prefix="/api/github",
    tags=["GitHub"]
)

app.include_router(
    linkedin_router,
    prefix="/api/linkedin",
    tags=["LinkedIn"]
)

app.include_router(
    leetcode_router,
    prefix="/api/leetcode",
    tags=["Leetcode"]
)

@app.get("/")
def home():
    return {"message": "Profile Analyzer API is running!"}