from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user import User
from src.auth.password import verify_password
from src.auth.jwt import create_access_token
from src.schemas.auth import LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login(
        request: LoginRequest,
        db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.username == request.username
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
            request.password,
            user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "Bearer"
    }