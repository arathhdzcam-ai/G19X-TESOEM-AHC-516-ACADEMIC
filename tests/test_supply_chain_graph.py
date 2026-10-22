from app.orchestration.supply_chain_graph import build_supply_chain_graph


def test_supply_chain_graph_completes_analysis():
    graph = build_supply_chain_graph()

    initial_state = {
        "product_id": "TEST-SKU-001",
        "historical_demand": [100, 120, 110, 130, 140],
        "forecast_periods": 3,
        "current_inventory": 100,
        "supplier_id": "TEST-SUP-001",
        "on_time_delivery_rate": 0.95,
        "quality_rate": 0.98,
        "supplier_capacity": 200,
    }

    result = graph.invoke(initial_state)

    assert "demand_result" in result
    assert "ai_demand_result" in result
    assert "forecast_comparison" in result
    assert "inventory_result" in result
    assert "supplier_result" in result
    assert "sourcing_result" in result
    assert "logistics_result" in result

    assert result["demand_result"]
    assert result["ai_demand_result"]
    assert result["supplier_result"]
    assert result["sourcing_result"]
    assert result["logistics_result"]

    if result["inventory_result"]["inventory_status"] == "low":
        assert result["purchasing_result"]


def test_supply_chain_graph_recommends_purchase_when_inventory_is_low():
    graph = build_supply_chain_graph()

    initial_state = {
        "product_id": "TEST-SKU-LOW",
        "historical_demand": [100, 120, 110, 130, 140],
        "forecast_periods": 3,
        "current_inventory": 10,
        "supplier_id": "TEST-SUP-001",
        "on_time_delivery_rate": 0.95,
        "quality_rate": 0.98,
        "supplier_capacity": 200,
    }

    result = graph.invoke(initial_state)

    assert result["inventory_result"]["inventory_status"] == "low"

    purchasing_result = result["purchasing_result"]

    assert purchasing_result["purchase_required"] is True
    assert purchasing_result["product_id"] == "TEST-SKU-LOW"
    assert purchasing_result["recommended_quantity"] > 0
    assert purchasing_result["action"] == "CREATE_PURCHASE_RECOMMENDATION"


def test_supply_chain_graph_skips_purchase_when_inventory_is_sufficient():
    graph = build_supply_chain_graph()

    initial_state = {
        "product_id": "TEST-SKU-OK",
        "historical_demand": [100, 120, 110, 130, 140],
        "forecast_periods": 3,
        "current_inventory": 1000,
        "supplier_id": "TEST-SUP-001",
        "on_time_delivery_rate": 0.95,
        "quality_rate": 0.98,
        "supplier_capacity": 200,
    }

    result = graph.invoke(initial_state)

    assert result["inventory_result"]["inventory_status"] == "sufficient"
    assert "purchasing_result" not in result



def test_supply_chain_graph_uses_traditional_forecast_when_ai_forecast_is_invalid(
    monkeypatch,
):
    import app.orchestration.supply_chain_graph as graph_module

    # Simular un agente de IA que no devuelve un pronóstico válido.
    class FakeAIDemandAgent:
        def analyze(self, historical_demand):
            return {
                "agent": "AIDemandAgent",
                "historical_demand": historical_demand,
                "method": "test_invalid_forecast",
                "fallback_used": False,
                "analysis": {
                    "average_demand": 120,
                    "forecast_demand": None,
                    "recommendation": "Prueba de pronóstico inválido.",
                },
            }

    monkeypatch.setattr(
        graph_module,
        "AIDemandAgent",
        FakeAIDemandAgent,
    )

    graph = build_supply_chain_graph()

    initial_state = {
        "product_id": "TEST-SKU-FALLBACK",
        "historical_demand": [100, 120, 110, 130, 140],
        "forecast_periods": 3,
        "current_inventory": 100,
        "supplier_id": "TEST-SUP-001",
        "on_time_delivery_rate": 0.95,
        "quality_rate": 0.98,
        "supplier_capacity": 200,
    }

    result = graph.invoke(initial_state)

    # El pronóstico tradicional debe utilizarse como respaldo.
    assert result["demand_result"]["forecast"][0] == 120
    assert result["forecast_comparison"]["ai_forecast"] == 120
    assert result["forecast_comparison"]["traditional_forecast"] == 120
    assert result["inventory_result"]["forecast_demand"] == 120
    assert result["sourcing_result"]["forecast_demand"] == 120
