
from app.agents.purchasing_agent import PurchasingAgent


def test_positive_quantity_recommends_purchase():
    agent = PurchasingAgent()

    result = agent.recommend_purchase(
        product_id="SKU-001",
        quantity=70
    )

    assert result["purchase_required"] is True
    assert result["product_id"] == "SKU-001"
    assert result["recommended_quantity"] == 70
    assert result["action"] == "CREATE_PURCHASE_RECOMMENDATION"


def test_zero_quantity_does_not_recommend_purchase():
    agent = PurchasingAgent()

    result = agent.recommend_purchase(
        product_id="SKU-001",
        quantity=0
    )

    assert result["purchase_required"] is False
    assert "message" in result


def test_negative_quantity_does_not_recommend_purchase():
    agent = PurchasingAgent()

    result = agent.recommend_purchase(
        product_id="SKU-001",
        quantity=-5
    )

    assert result["purchase_required"] is False
    assert "message" in result
