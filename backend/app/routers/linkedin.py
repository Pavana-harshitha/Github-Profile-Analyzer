from fastapi import APIRouter, UploadFile, File
from app.services.linkedin_service import analyze_linkedin_pdf

router = APIRouter()


@router.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):

    result = analyze_linkedin_pdf(file.file)
    print(result)
    return {
        "analysis": result
    }