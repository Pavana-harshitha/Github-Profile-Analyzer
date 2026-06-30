from fastapi import FastAPI
from app.routers.github import router as github_router

app = FastAPI()

app.include_router(
    github_router,
    prefix="/api/github",
    tags=["GitHub"]
)

@app.get("/")
def root():
    return {"message": "GitHub Profile Analyzer API is running!"}