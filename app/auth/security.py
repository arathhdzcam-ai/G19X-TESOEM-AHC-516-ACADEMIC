
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.auth.config import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Genera un hash seguro de una contraseña."""
    return password_hash.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    """Comprueba una contraseña sin almacenarla en texto plano."""
    try:
        return password_hash.verify(password, stored_hash)
    except Exception:
        return False


def create_access_token(user_id: int, email: str) -> str:
    """Genera un JWT con identificador, correo y vencimiento."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Valida la firma, el algoritmo y el vencimiento del JWT."""
    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
        options={"require": ["sub", "exp", "iat"]},
    )
