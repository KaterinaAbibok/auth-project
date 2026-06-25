from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.document import Document
from src.auth.authorization import require_permission
from src.schemas.document import DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

document_read_permission = require_permission("DOCUMENT", "READ")


@router.get("", response_model=list[DocumentResponse])
def get_documents(
    current_user=Depends(document_read_permission),
    db: Session = Depends(get_db)
):
    return db.query(Document).all()