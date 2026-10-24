
import os
from pathlib import Path

from dotenv import load_dotenv

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Cargar las variables de .env antes de leer la configuración.
# override=False conserva las variables ya definidas en Windows.
load_dotenv(PROJECT_ROOT / ".env", override=False)

# Base de datos local SQLite
DATABASE_PATH = PROJECT_ROOT / "supplychain_users.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Clave secreta JWT: debe configurarse fuera del código
JWT_SECRET_KEY = os.getenv("SUPPLYCHAIN_JWT_SECRET")

if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32:
    raise RuntimeError(
        "Configura SUPPLYCHAIN_JWT_SECRET con una clave "
        "aleatoria de al menos 32 caracteres."
    )

# Configuración del token
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 30
