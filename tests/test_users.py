from fastapi import HTTPException

from src.main import app
from src.models.user import User
from src.models.role import Role
from src.routers.users import (
    user_read_permission,
    user_update_permission,
    user_delete_permission
)
from src.auth.password import hash_password

def test_get_users_success(client, db_session):
    role = Role(name="USER")
    db_session.add(role)
    db_session.commit()

    user = User(
        username="kate",
        password_hash=hash_password("123"),
        is_active=True
    )
    user.roles.append(role)

    db_session.add(user)
    db_session.commit()

    def override_permission():
        return user

    app.dependency_overrides[user_read_permission] = override_permission

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) >= 1

    app.dependency_overrides.clear()

def test_get_users_forbidden(client):
    def override_permission():
        raise HTTPException(status_code=403, detail="Forbidden")

    app.dependency_overrides[user_read_permission] = override_permission

    response = client.get("/users")

    assert response.status_code == 403

    app.dependency_overrides.clear()

def test_create_user_success(client, db_session):
    role = Role(name="USER")
    db_session.add(role)
    db_session.commit()

    admin = User(
        username="admin",
        password_hash=hash_password("123"),
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()

    def override_permission():
        return admin

    app.dependency_overrides[user_update_permission] = override_permission

    response = client.post(
        "/users",
        json={
            "username": "new_user",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "new_user"

    app.dependency_overrides.clear()

def test_create_user_duplicate(client, db_session):
    role = Role(name="USER")
    db_session.add(role)
    db_session.commit()

    admin = User(
        username="admin",
        password_hash=hash_password("123"),
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()

    existing = User(
        username="existing",
        password_hash=hash_password("123"),
        is_active=True
    )
    existing.roles.append(role)
    db_session.add(existing)
    db_session.commit()

    def override_permission():
        return admin

    app.dependency_overrides[user_update_permission] = override_permission

    response = client.post(
        "/users",
        json={
            "username": "existing",
            "password": "123456"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

    app.dependency_overrides.clear()


def test_delete_user_success(client, db_session):
    role = Role(name="USER")
    db_session.add(role)
    db_session.commit()

    admin = User(
        username="admin",
        password_hash=hash_password("123"),
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()

    user = User(
        username="to_delete",
        password_hash=hash_password("123"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    def override_permission():
        return admin

    app.dependency_overrides[user_delete_permission] = override_permission

    response = client.delete(f"/users/{user.id}")

    assert response.status_code == 200
    assert "deactivated" in response.json()["message"]

    db_session.refresh(user)
    assert user.is_active is False

    app.dependency_overrides.clear()


def test_delete_user_forbidden(client):
    def override_permission():
        raise HTTPException(status_code=403, detail="Forbidden")

    app.dependency_overrides[user_delete_permission] = override_permission

    response = client.delete("/users/1")

    assert response.status_code == 403

    app.dependency_overrides.clear()