from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from src.db import get_db

from src.models.user import User
from src.models.role import Role
from src.models.permission import Permission

router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get("")
def seed(db: Session = Depends(get_db)):
    admin_role = Role(
        name="ADMIN"
    )

    user_role = Role(
        name="USER"
    )

    db.add(admin_role)
    db.add(user_role)

    p1 = Permission(
        resource="DOCUMENT",
        action="READ"
    )

    p2 = Permission(
        resource="DOCUMENT",
        action="UPDATE"
    )

    p3 = Permission(
        resource="USER",
        action="READ"
    )

    p4 = Permission(
        resource="USER",
        action="DELETE"
    )

    db.add_all([
        p1,
        p2,
        p3,
        p4
    ])

    admin_role.permissions.extend([
        p1,
        p2,
        p3,
        p4
    ])
    user_role.permissions.append(
        p1
    )
    user = (
        db.query(User)
        .filter(User.id == 1)
        .first()
    )
    user.roles.append(admin_role)
    user.roles.append(user_role)
    db.commit()

    return {
        "message": "seed completed"
    }