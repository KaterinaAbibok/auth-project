from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from src.db import get_db

from src.models.user import User
from src.models.role import Role
from src.models.permission import Permission
from src.auth.password import hash_password

router = APIRouter(
    prefix="/seed",
    tags=["seed"]
)

@router.post("")
def seed(db: Session = Depends(get_db)):
    if db.query(Role).first():
        return {
            "message": "Seed data already exists"
        }

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
    admin = User(
        username="admin@test.com",
        password_hash=hash_password("admin123"),
        is_active=True
    )

    user1 = User(
        username="user1@test.com",
        password_hash=hash_password("user123"),
        is_active=True
    )

    user2 = User(
        username="user2@test.com",
        password_hash=hash_password("user123"),
        is_active=True
    )

    db.add_all([
        admin_role,
        user_role,
        admin,
        user1,
        user2
    ])

    admin.roles.append(admin_role)

    user1.roles.append(user_role)
    user2.roles.append(user_role)
    db.commit()

    return {
        "message": "seed completed"
    }