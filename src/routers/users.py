from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user import User
from src.models.role import Role
from src.schemas.user import UserCreate
from src.schemas.user import UserResponse

from src.auth.password import hash_password
from src.auth.authorization import require_permission

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

user_read_permission = require_permission("USER", "READ")
user_update_permission = require_permission("USER", "UPDATE")
user_delete_permission = require_permission("USER", "DELETE")

@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    current_user=Depends(user_read_permission),
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
        current_user=Depends(user_update_permission),
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

    user_role = db.query(Role).filter(Role.name == "USER").first()
    if not user_role:
        raise ValueError("Role USER not found in DB")
    user.roles.append(user_role)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(user_delete_permission),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()

    return {
        "message": f"User {user_id} deactivated"
    }