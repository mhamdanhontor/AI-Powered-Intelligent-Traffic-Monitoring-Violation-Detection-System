from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    video: dict