
import re
import sqlite3

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.auth.database import get_db_connection
from app.auth.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


class RegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    email = str(request.email).lower()

    # Evita correos con formatos excesivamente largos.
    if len(email) > 254:
        raise HTTPException(
            status_code=422,
            detail="El correo electrónico es demasiado largo.",
        )

    password_digest = hash_password(request.password)

    try:
        with get_db_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (?, ?)
                """,
                (email, password_digest),
            )
            user_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo registrar la cuenta con esos datos.",
        )

    return {
        "message": "Cuenta creada correctamente.",
        "user_id": user_id,
        "email": email,
    }


@router.post("/login")
def login(request: LoginRequest):
    email = str(request.email).lower()

    with get_db_connection() as connection:
        user = connection.execute(
            """
            SELECT id, email, password_hash, is_active
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    # Mensaje genérico para no revelar si la cuenta existe.
    if user is None or not verify_password(
        request.password,
        user["password_hash"] if user else "",
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta está desactivada.",
        )

    token = create_access_token(
        user_id=user["id"],
        email=user["email"],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 1800,
    }
