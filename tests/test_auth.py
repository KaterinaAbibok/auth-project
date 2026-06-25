from unittest.mock import patch

from src.models.user import User


def test_login_success(client, db_session):
    user = User(
        username="user",
        password_hash="hashed_password",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    with patch("src.routers.auth.verify_password", return_value=True), \
         patch("src.routers.auth.create_access_token", return_value="test-token"):
        response = client.post(
            "/auth/login",
            json={
                "username": "user",
                "password": "123456"
            }
        )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test-token",
        "token_type": "Bearer"
    }


def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "unknown",
            "password": "123456"
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }


def test_login_inactive_user(client, db_session):
    user = User(
        username="user",
        password_hash="hashed_password",
        is_active=False
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": "user",
            "password": "123456"
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "User is inactive"
    }


def test_login_wrong_password(client, db_session):
    user = User(
        username="user",
        password_hash="hashed_password",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    with patch("src.routers.auth.verify_password", return_value=False):
        response = client.post(
            "/auth/login",
            json={
                "username": "user",
                "password": "wrong-password"
            }
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }