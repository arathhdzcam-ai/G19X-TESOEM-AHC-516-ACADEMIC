
from app.agents.supplier_monitoring_agent import SupplierMonitoringAgent


def test_supplier_with_late_deliveries_has_medium_risk():
    agent = SupplierMonitoringAgent()

    result = agent.analyze(
        supplier_id="SUP-001",
        on_time_delivery_rate=0.88,
        quality_rate=0.97,
        capacity=500
    )

    assert result["supplier_id"] == "SUP-001"
    assert result["risk"] == "medium"
    assert result["risk_factors"] == 1


def test_supplier_with_good_metrics_has_low_risk():
    agent = SupplierMonitoringAgent()

    result = agent.analyze(
        supplier_id="SUP-002",
        on_time_delivery_rate=0.98,
        quality_rate=0.99,
        capacity=500
    )

    assert result["risk"] == "low"
    assert result["risk_factors"] == 0