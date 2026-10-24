
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.auth.dependencies import get_current_user
from app import main
from app import supply_chain_database as db


@pytest.fixture
def api_client(tmp_path, monkeypatch):
    # Usar una base de datos temporal para no alterar los datos reales.
    test_db = tmp_path / "supply_chain_api_test.db"

    monkeypatch.setattr(db, "SUPPLY_CHAIN_DATABASE_PATH", test_db)
    monkeypatch.setattr(
        main,
        "save_supply_chain_analysis",
        db.save_supply_chain_analysis,
    )
    monkeypatch.setattr(
        main,
        "get_supply_chain_analysis",
        db.get_supply_chain_analysis,
    )
    monkeypatch.setattr(
        main,
        "list_supply_chain_analyses",
        db.list_supply_chain_analyses,
    )

    db.initialize_supply_chain_database()

    # Simular un usuario autenticado, sin modificar el login.
    app.dependency_overrides[get_current_user] = (
        lambda: {"id": 1, "email": "test@example.com"}
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(get_current_user, None)


def fake_graph_result(state):
    return {
        "product_id": state["product_id"],
        "demand_result": {
            "average_demand": 120,
            "forecast": [120, 120, 120],
        },
        "ai_demand_result": {
            "forecast_demand": 150,
        },
        "forecast_comparison": {
            "difference": 30,
        },
        "inventory_result": {
            "current_inventory": state["current_inventory"],
            "status": "low",
        },
        "supplier_result": {
            "supplier_id": state["supplier_id"],
            "risk": "low",
        },
        "sourcing_result": {},
        "logistics_result": {},
        "purchasing_result": {
            "recommended_quantity": 70,
        },
    }


class FakeGraph:
    def invoke(self, state):
        return fake_graph_result(state)


def valid_payload():
    return {
        "product_id": "API-TEST-001",
        "historical_demand": [100, 120, 110, 130, 140],
        "forecast_periods": 3,
        "current_inventory": 100,
        "supplier_id": "SUP-TEST-001",
        "on_time_delivery_rate": 0.95,
        "quality_rate": 0.98,
        "supplier_capacity": 200,
    }


def test_analyze_saves_result_and_returns_id(api_client, monkeypatch):
    monkeypatch.setattr(
        main,
        "build_supply_chain_graph",
        lambda: FakeGraph(),
    )

    response = api_client.post(
        "/api/supply-chain/analyze",
        json=valid_payload(),
    )

    assert response.status_code == 200

    data = response.json()
    assert data["product_id"] == "API-TEST-001"
    assert isinstance(data["analysis_id"], int)
    assert data["analysis_id"] > 0
    assert data["demand_analysis"]["average_demand"] == 120


def test_history_contains_saved_analysis(api_client, monkeypatch):
    monkeypatch.setattr(
        main,
        "build_supply_chain_graph",
        lambda: FakeGraph(),
    )

    created = api_client.post(
        "/api/supply-chain/analyze",
        json=valid_payload(),
    )
    assert created.status_code == 200

    response = api_client.get("/api/supply-chain/history")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["items"][0]["product_id"] == "API-TEST-001"


def test_get_analysis_by_id(api_client, monkeypatch):
    monkeypatch.setattr(
        main,
        "build_supply_chain_graph",
        lambda: FakeGraph(),
    )

    created = api_client.post(
        "/api/supply-chain/analyze",
        json=valid_payload(),
    )
    analysis_id = created.json()["analysis_id"]

    response = api_client.get(
        f"/api/supply-chain/history/{analysis_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == analysis_id
    assert response.json()["product_id"] == "API-TEST-001"


def test_get_missing_analysis_returns_404(api_client):
    response = api_client.get("/api/supply-chain/history/999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": 101},
        {"offset": -1},
    ],
)
def test_history_rejects_invalid_pagination(api_client, params):
    response = api_client.get(
        "/api/supply-chain/history",
        params=params,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("product_id", "string"),
        ("supplier_id", "string"),
        ("product_id", "   "),
        ("supplier_id", "   "),
    ],
)
def test_analyze_rejects_invalid_identifiers(
    api_client,
    field,
    invalid_value,
):
    payload = valid_payload()
    payload[field] = invalid_value

    response = api_client.post(
        "/api/supply-chain/analyze",
        json=payload,
    )

    assert response.status_code == 422

def test_api_history_is_isolated_between_users(api_client, monkeypatch):
    monkeypatch.setattr(
        main,
        "build_supply_chain_graph",
        lambda: FakeGraph(),
    )

    # El usuario 1 crea un análisis.
    created = api_client.post(
        "/api/supply-chain/analyze",
        json=valid_payload(),
    )
    assert created.status_code == 200
    analysis_id = created.json()["analysis_id"]

    # Cambiamos al usuario 2 sin modificar el sistema de login.
    app.dependency_overrides[get_current_user] = (
        lambda: {"id": 2, "email": "other@example.com"}
    )

    # El historial del usuario 2 no debe mostrar el análisis del usuario 1.
    history = api_client.get("/api/supply-chain/history")
    assert history.status_code == 200
    assert history.json()["count"] == 0
    assert history.json()["items"] == []

    # Tampoco debe poder consultar directamente ese análisis.
    detail = api_client.get(
        f"/api/supply-chain/history/{analysis_id}"
    )
    assert detail.status_code == 404