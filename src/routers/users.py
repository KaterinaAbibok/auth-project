from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user import User
from src.schemas.user import UserCreate
from src.schemas.user import UserResponse

from src.auth.password import hash_password
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return users


@router.post(
    "",
    response_model=UserResponse
)
def create_user(
        request: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.username == request.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user = User(
        username=request.username,
        password_hash=hash_password(
            request.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user