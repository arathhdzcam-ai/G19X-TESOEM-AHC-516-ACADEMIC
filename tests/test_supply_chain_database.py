
import pytest

from app import supply_chain_database as db


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    test_db = tmp_path / "supply_chain_test.db"

    monkeypatch.setattr(
        db,
        "SUPPLY_CHAIN_DATABASE_PATH",
        test_db,
    )

    db.initialize_supply_chain_database()
    return test_db


def sample_analysis():
    return {
        "product_id": "TEST-PERSIST-001",
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

    analysis_id = db.save_supply_chain_analysis(original)
    recovered = db.get_supply_chain_analysis(analysis_id)

    assert analysis_id == 1
    assert recovered is not None
    assert recovered["id"] == analysis_id
    assert recovered["product_id"] == "TEST-PERSIST-001"
    assert recovered["supplier_id"] == "SUP-TEST-001"
    assert recovered["result"] == original
    assert recovered["created_at"]


def test_get_analysis_returns_none_when_not_found(temporary_database):
    assert db.get_supply_chain_analysis(999) is None


def test_list_analyses_supports_pagination(temporary_database):
    for product_id in ["PRODUCT-A", "PRODUCT-B", "PRODUCT-C"]:
        db.save_supply_chain_analysis({
            "product_id": product_id,
            "supplier_analysis": {"supplier_id": "SUP-001"},
        })

    first_page = db.list_supply_chain_analyses(limit=2, offset=0)
    second_page = db.list_supply_chain_analyses(limit=2, offset=2)

    assert len(first_page) == 2
    assert len(second_page) == 1
    assert first_page[0]["product_id"] == "PRODUCT-C"
    assert first_page[1]["product_id"] == "PRODUCT-B"
    assert second_page[0]["product_id"] == "PRODUCT-A"


def test_save_requires_product_id(temporary_database):
    with pytest.raises(ValueError, match="product_id"):
        db.save_supply_chain_analysis({
            "supplier_analysis": {"supplier_id": "SUP-001"}
        })


@pytest.mark.parametrize("limit", [0, 101, -1])
def test_list_rejects_invalid_limit(temporary_database, limit):
    with pytest.raises(ValueError, match="limit"):
        db.list_supply_chain_analyses(limit=limit)


@pytest.mark.parametrize("offset", [-1, -10])
def test_list_rejects_negative_offset(temporary_database, offset):
    with pytest.raises(ValueError, match="offset"):
        db.list_supply_chain_analyses(offset=offset)
