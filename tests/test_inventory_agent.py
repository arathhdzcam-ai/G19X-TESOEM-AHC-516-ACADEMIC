
from app.agents.inventory_agent import InventoryAgent


def test_low_inventory_recommends_order():
    agent = InventoryAgent(safety_stock=20)

    result = agent.analyze(
        current_inventory=100,
        forecast_demand=150
    )

    assert result["inventory_status"] == "low"
    assert result["required_inventory"] == 170
    assert result["recommended_order"] == 70


def test_sufficient_inventory_does_not_recommend_order():
    agent = InventoryAgent(safety_stock=20)

    result = agent.analyze(
        current_inventory=200,
        forecast_demand=150
    )

    assert result["inventory_status"] == "sufficient"
    assert result["required_inventory"] == 170
    assert result["recommended_order"] == 0


def test_inventory_exactly_at_requirement_is_sufficient():
    agent = InventoryAgent(safety_stock=20)

    result = agent.analyze(
        current_inventory=170,
        forecast_demand=150
    )

    assert result["inventory_status"] == "sufficient"
    assert result["recommended_order"] == 0