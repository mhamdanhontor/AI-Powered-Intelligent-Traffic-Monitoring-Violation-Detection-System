from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile, HTTPException

from app.config import UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}


def save_uploaded_video(file: UploadFile):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format."
        )

    filename = f"{uuid4().hex}{extension}"

    file_path = UPLOAD_FOLDER / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": filename,
        "path": str(file_path),
        "original_name": file.filename
    }