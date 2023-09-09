from pydantic import BaseModel

class CreateUploadedFileSchema(BaseModel):
    file_path: str
