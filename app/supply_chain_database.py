
import json
import sqlite3

from datetime import datetime, timezone
from pathlib import Path


# Base de datos independiente para los datos de Supply Chain.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUPPLY_CHAIN_DATABASE_PATH = PROJECT_ROOT / "supply_chain_data.db"


def initialize_supply_chain_database():
    """Crea la tabla de historial de análisis si no existe."""
    with sqlite3.connect(SUPPLY_CHAIN_DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS supply_chain_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                supplier_id TEXT,
                created_at TEXT NOT NULL,
                result_json TEXT NOT NULL
            )
            """
        )


def save_supply_chain_analysis(result: dict) -> int:
    """Guarda el resultado completo y devuelve su identificador."""
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
                result_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (product_id, supplier_id, created_at, result_json),
        )

        return cursor.lastrowid



def get_supply_chain_analysis(analysis_id: int) -> dict | None:
    """Recupera un análisis guardado por su identificador."""
    with sqlite3.connect(SUPPLY_CHAIN_DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT id, product_id, supplier_id, created_at, result_json
            FROM supply_chain_analyses
            WHERE id = ?
            """,
            (analysis_id,),
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
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    """Recupera el historial de análisis con paginación."""
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
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
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
