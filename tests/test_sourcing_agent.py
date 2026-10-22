import pytest

from app.agents.sourcing_agent import SourcingAgent


def test_sufficient_inventory():
    result = SourcingAgent().analyze(
        product_id="SKU-001",
        forecast_demand=100,
        current_inventory=150,
        safety_stock=20,
        supplier_capacity=200,
    )

    assert result["status"] == "sufficient"
    assert result["shortage"] == 0
    assert result["recommended_quantity"] == 0


def test_replenishment_required():
    result = SourcingAgent().analyze(
        product_id="SKU-001",
        forecast_demand=100,
        current_inventory=50,
        safety_stock=20,
        supplier_capacity=200,
    )

    assert result["status"] == "replenishment_required"
    assert result["shortage"] == 70
    assert result["recommended_quantity"] == 70


def test_insufficient_supplier_capacity():
    result = SourcingAgent().analyze(
        product_id="SKU-001",
        forecast_demand=100,
        current_inventory=50,
        safety_stock=20,
        supplier_capacity=30,
    )

    assert result["status"] == "insufficient_supplier_capacity"
    assert result["recommended_quantity"] == 30
    assert result["unmet_quantity"] == 40


def test_empty_product_id_is_rejected():
    with pytest.raises(ValueError):
        SourcingAgent().analyze(
            product_id=" ",
            forecast_demand=100,
            current_inventory=50,
            safety_stock=20,
            supplier_capacity=200,
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("forecast_demand", -1),
        ("current_inventory", -1),
        ("safety_stock", -1),
        ("supplier_capacity", -1),
    ],
)
def test_negative_values_are_rejected(field, value):
    data = {
        "product_id": "SKU-001",
        "forecast_demand": 100,
        "current_inventory": 50,
        "safety_stock": 20,
        "supplier_capacity": 200,
    }
    data[field] = value

    with pytest.raises(ValueError):
        SourcingAgent().analyze(**data)
