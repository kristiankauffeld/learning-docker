from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models, schemas

def create_uploaded_file(db: Session, uploaded_file: schemas.CreateUploadedFileSchema):
    try:
        db_item = models.UploadedFileModel(file_path=uploaded_file.file_path)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        db.rollback()
        print("An error occurred:", str(e))
        raise e
