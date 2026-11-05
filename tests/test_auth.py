
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.auth import database
from app.auth.database import initialize_database, get_db_connection
from app.auth.security import hash_password


@pytest.fixture
def auth_client(tmp_path, monkeypatch):
    # Crear una base de datos temporal para las pruebas.
    test_db = tmp_path / "auth_test.db"

    # Sustituir la ruta de la base de datos real.
    monkeypatch.setattr(database, "DATABASE_PATH", test_db)

    # Inicializar la tabla de usuarios.
    initialize_database()

    with TestClient(app) as client:
        yield client


def create_user(email, password, is_active=1):
    # Crear un usuario de prueba.
    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO users (email, password_hash, is_active)
            VALUES (?, ?, ?)
            """,
            (email, hash_password(password), is_active),
        )


def test_login_returns_token_and_user_data(auth_client):
    create_user("test@example.com", "PasswordSeguro123!")

    response = auth_client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "PasswordSeguro123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800
    assert isinstance(data["user_id"], int)
    assert data["user_id"] > 0
    assert data["email"] == "test@example.com"


def test_login_rejects_incorrect_password(auth_client):
    create_user("test@example.com", "PasswordSeguro123!")

    response = auth_client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "Incorrecta123!",
        },
    )

    assert response.status_code == 401


def test_login_rejects_inactive_account(auth_client):
    create_user(
        "inactive@example.com",
        "PasswordSeguro123!",
        is_active=0,
    )

    response = auth_client.post(
        "/api/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "PasswordSeguro123!",
        },
    )

    assert response.status_code == 403
