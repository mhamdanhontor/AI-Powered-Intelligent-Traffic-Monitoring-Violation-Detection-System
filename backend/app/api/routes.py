from fastapi import APIRouter, UploadFile, File

from app.services.upload_service import save_uploaded_video

router = APIRouter()


@router.get("/")
async def home():
    return {
        "project": "AI Traffic Analysis System",
        "version": "1.0.0",
        "status": "Running"
    }


@router.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    result = save_uploaded_video(file)

    return {
        "message": "Video uploaded successfully",
        "video": result
    }