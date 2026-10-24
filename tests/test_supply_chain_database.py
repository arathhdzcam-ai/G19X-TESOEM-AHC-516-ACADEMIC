
import sqlite3

import pytest

from app import supply_chain_database as db


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    test_db = tmp_path / "supply_chain_test.db"
    monkeypatch.setattr(db, "SUPPLY_CHAIN_DATABASE_PATH", test_db)
    db.initialize_supply_chain_database()
    return test_db


def sample_analysis(product_id="TEST-PERSIST-001"):
    return {
        "product_id": product_id,
        "supplier_analysis": {
            "supplier_id": "SUP-TEST-001",
            "risk": "low",
        },
        "demand_analysis": {
            "average_demand": 120,
            "forecast": [120, 120, 120],
        },
    }


def test_save_and_retrieve_analysis(temporary_database):
    original = sample_analysis()
    analysis_id = db.save_supply_chain_analysis(original, user_id=1)

    recovered = db.get_supply_chain_analysis(analysis_id, user_id=1)

    assert analysis_id == 1
    assert recovered is not None
    assert recovered["id"] == analysis_id
    assert recovered["product_id"] == "TEST-PERSIST-001"
    assert recovered["supplier_id"] == "SUP-TEST-001"
    assert recovered["result"] == original
    assert recovered["created_at"]


def test_get_analysis_returns_none_when_not_found(temporary_database):
    assert db.get_supply_chain_analysis(999, user_id=1) is None


def test_user_cannot_retrieve_another_users_analysis(temporary_database):
    analysis_id = db.save_supply_chain_analysis(
        sample_analysis(),
        user_id=1,
    )

    assert db.get_supply_chain_analysis(analysis_id, user_id=2) is None


def test_list_analyses_supports_pagination(temporary_database):
    for product_id in ["PRODUCT-A", "PRODUCT-B", "PRODUCT-C"]:
        db.save_supply_chain_analysis(
            sample_analysis(product_id),
            user_id=1,
        )

    first_page = db.list_supply_chain_analyses(
        user_id=1,
        limit=2,
        offset=0,
    )
    second_page = db.list_supply_chain_analyses(
        user_id=1,
        limit=2,
        offset=2,
    )

    assert len(first_page) == 2
    assert len(second_page) == 1
    assert first_page[0]["product_id"] == "PRODUCT-C"
    assert first_page[1]["product_id"] == "PRODUCT-B"
    assert second_page[0]["product_id"] == "PRODUCT-A"


def test_list_analyses_only_returns_current_users_records(
    temporary_database,
):
    db.save_supply_chain_analysis(sample_analysis("USER-1"), user_id=1)
    db.save_supply_chain_analysis(sample_analysis("USER-2"), user_id=2)

    user_one_records = db.list_supply_chain_analyses(user_id=1)
    user_two_records = db.list_supply_chain_analyses(user_id=2)

    assert [item["product_id"] for item in user_one_records] == ["USER-1"]
    assert [item["product_id"] for item in user_two_records] == ["USER-2"]


def test_save_requires_product_id(temporary_database):
    with pytest.raises(ValueError, match="product_id"):
        db.save_supply_chain_analysis(
            {"supplier_analysis": {"supplier_id": "SUP-001"}},
            user_id=1,
        )


@pytest.mark.parametrize("limit", [0, 101, -1])
def test_list_rejects_invalid_limit(temporary_database, limit):
    with pytest.raises(ValueError, match="limit"):
        db.list_supply_chain_analyses(user_id=1, limit=limit)


@pytest.mark.parametrize("offset", [-1, -10])
def test_list_rejects_negative_offset(temporary_database, offset):
    with pytest.raises(ValueError, match="offset"):
        db.list_supply_chain_analyses(user_id=1, offset=offset)


def test_initialization_migrates_existing_table_without_deleting_records(
    tmp_path,
    monkeypatch,
):
    test_db = tmp_path / "legacy_supply_chain.db"
    monkeypatch.setattr(db, "SUPPLY_CHAIN_DATABASE_PATH", test_db)

    # Simula la tabla antigua, que todavía no tenía user_id.
    with sqlite3.connect(test_db) as connection:
        connection.execute(
            """
            CREATE TABLE supply_chain_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                supplier_id TEXT,
                created_at TEXT NOT NULL,
                result_json TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            INSERT INTO supply_chain_analyses (
                product_id, supplier_id, created_at, result_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "LEGACY-001",
                "SUP-OLD",
                "2026-01-01T00:00:00+00:00",
                '{"product_id": "LEGACY-001"}',
            ),
        )

    db.initialize_supply_chain_database()

    with sqlite3.connect(test_db) as connection:
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(supply_chain_analyses)"
            ).fetchall()
        }
        legacy_row = connection.execute(
            """
            SELECT product_id, user_id
            FROM supply_chain_analyses
            WHERE id = 1
            """
        ).fetchone()

    assert "user_id" in columns
    assert legacy_row == ("LEGACY-001", None)

    # Los registros heredados se conservan, pero no se asignan
    # automáticamente a ningún usuario.
    assert db.get_supply_chain_analysis(1, user_id=1) is None
    assert db.list_supply_chain_analyses(user_id=1) == []
