
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.database import get_db_connection
from app.auth.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o sesión expirada.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])

        if user_id <= 0:
            raise unauthorized

    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise unauthorized

    with get_db_connection() as connection:
        user = connection.execute(
            "SELECT id, email, is_active FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    if user is None:
        raise unauthorized

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta está desactivada.",
        )

    return {
        "id": user["id"],
        "email": user["email"],
    }
