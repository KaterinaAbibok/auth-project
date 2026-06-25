from fastapi import HTTPException

from src.main import app
from src.models.document import Document
from src.models.user import User
from src.routers.documents import document_read_permission


def test_get_documents_success(client, db_session):
    user = User(
        username="kate",
        password_hash="hash",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    doc1 = Document(type="Doc 1")
    doc2 = Document(type="Doc 2")
    db_session.add_all([doc1, doc2])
    db_session.commit()

    def override_permission():
        return user

    app.dependency_overrides[document_read_permission] = override_permission

    response = client.get("/documents")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    app.dependency_overrides.clear()


def test_get_documents_forbidden(client):
    def override_permission():
        raise HTTPException(status_code=403, detail="Forbidden")

    app.dependency_overrides[document_read_permission] = override_permission

    response = client.get("/documents")

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    app.dependency_overrides.clear()


def test_get_documents_unauthorized(client):
    def override_permission():
        raise HTTPException(status_code=401, detail="Not authenticated")

    app.dependency_overrides[document_read_permission] = override_permission

    response = client.get("/documents")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    app.dependency_overrides.clear()