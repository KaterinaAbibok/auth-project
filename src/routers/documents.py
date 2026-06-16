from fastapi import APIRouter
from fastapi import Depends

from src.auth.authorization import require_permission

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

DOCUMENTS = [
    {
        "id": 1,
        "title": "Contract"
    },
    {
        "id": 2,
        "title": "Invoice"
    }
]

@router.get("")
def get_documents(
    current_user=Depends(
        require_permission(
            "DOCUMENT",
            "READ"
        )
    )
):
    return DOCUMENTS