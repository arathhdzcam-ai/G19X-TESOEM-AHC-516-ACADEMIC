
import json
import sqlite3

from datetime import datetime, timezone
from pathlib import Path


# Base de datos independiente para los datos de Supply Chain.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUPPLY_CHAIN_DATABASE_PATH = PROJECT_ROOT / "supply_chain_data.db"


def initialize_supply_chain_database():
    """Crea o actualiza la tabla de historial sin eliminar registros."""
    with sqlite3.connect(SUPPLY_CHAIN_DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS supply_chain_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                supplier_id TEXT,
                created_at TEXT NOT NULL,
                result_json TEXT NOT NULL,
                user_id INTEGER
            )
            """
        )

        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(supply_chain_analyses)"
            ).fetchall()
        }

        # Los registros anteriores conservan sus datos.
        # Su propietario queda sin asignar hasta una migración segura.
        if "user_id" not in columns:
            connection.execute(
                "ALTER TABLE supply_chain_analyses "
                "ADD COLUMN user_id INTEGER"
            )


def _validate_user_id(user_id: int) -> None:
    if (
        not isinstance(user_id, int)
        or isinstance(user_id, bool)
        or user_id <= 0
    ):
        raise ValueError("user_id debe ser un entero positivo.")


def save_supply_chain_analysis(result: dict, user_id: int) -> int:
    """Guarda un análisis asociado al usuario autenticado."""
    _validate_user_id(user_id)

    product_id = result.get("product_id")

    if not product_id:
        raise ValueError("El resultado debe incluir product_id.")

    supplier_analysis = result.get("supplier_analysis") or {}
    supplier_id = supplier_analysis.get("supplier_id")

    created_at = datetime.now(timezone.utc).isoformat()
    result_json = json.dumps(result, ensure_ascii=False)

    with sqlite3.connect(SUPPLY_CHAIN_DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO supply_chain_analyses (
                product_id,
                supplier_id,
                created_at,
                result_json,
                user_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (product_id, supplier_id, created_at, result_json, user_id),
        )

        return cursor.lastrowid


def get_supply_chain_analysis(
    analysis_id: int,
    user_id: int,
) -> dict | None:
    """Recupera un análisis únicamente si pertenece al usuario."""
    _validate_user_id(user_id)

    with sqlite3.connect(SUPPLY_CHAIN_DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT id, product_id, supplier_id, created_at, result_json
            FROM supply_chain_analyses
            WHERE id = ? AND user_id = ?
            """,
            (analysis_id, user_id),
        ).fetchone()

    if row is None:
        return None

    return {
        "id": row["id"],
        "product_id": row["product_id"],
        "supplier_id": row["supplier_id"],
        "created_at": row["created_at"],
        "result": json.loads(row["result_json"]),
    }


def list_supply_chain_analyses(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    """Lista únicamente los análisis del usuario autenticado."""
    _validate_user_id(user_id)

    if not 1 <= limit <= 100:
        raise ValueError("limit debe estar entre 1 y 100.")

    if offset < 0:
        raise ValueError("offset no puede ser negativo.")

    with sqlite3.connect(SUPPLY_CHAIN_DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT id, product_id, supplier_id, created_at, result_json
            FROM supply_chain_analyses
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset),
        ).fetchall()

    return [
        {
            "id": row["id"],
            "product_id": row["product_id"],
            "supplier_id": row["supplier_id"],
            "created_at": row["created_at"],
            "result": json.loads(row["result_json"]),
        }
        for row in rows
    ]
