
import json
from types import SimpleNamespace

import app.agents.ai_demand_agent as ai_demand_module
from app.agents.ai_demand_agent import AIDemandAgent


def test_ai_demand_returns_analysis(monkeypatch):
    # Simular una respuesta de Azure OpenAI sin llamar al servicio real.
    expected_analysis = {
        "trend": "creciente",
        "average_demand": 120,
        "forecast_demand": 150,
        "demand_variability": "media",
        "risk": "medio",
        "recommendation": "Monitorear la demanda y ajustar el inventario."
    }

    def fake_create(**kwargs):
        return SimpleNamespace(
            output_text=json.dumps(expected_analysis)
        )

    fake_client = SimpleNamespace(
        responses=SimpleNamespace(create=fake_create)
    )

    monkeypatch.setattr(
        ai_demand_module,
        "client",
        fake_client
    )

    agent = AIDemandAgent()

    result = agent.analyze(
        historical_demand=[100, 120, 110, 130, 140]
    )

    assert isinstance(result, dict)
    assert result["agent"] == "AIDemandAgent"
    assert "analysis" in result
    assert isinstance(result["analysis"], dict)
    assert "recommendation" in result["analysis"]
    assert result["analysis"]["average_demand"] == 120
    assert result["analysis"]["forecast_demand"] == 150



def test_ai_demand_uses_fallback_when_azure_fails(monkeypatch):
    # Simular un error de conexión con Azure OpenAI.
    def fake_create(**kwargs):
        raise RuntimeError("Azure OpenAI no disponible")

    fake_client = SimpleNamespace(
        responses=SimpleNamespace(create=fake_create)
    )

    monkeypatch.setattr(
        ai_demand_module,
        "client",
        fake_client
    )

    agent = AIDemandAgent()

    result = agent.analyze(
        historical_demand=[100, 120, 110, 130, 140]
    )

    # El agente debe recuperarse y usar el promedio histórico.
    assert result["agent"] == "AIDemandAgent"
    assert result["method"] == "historical_average_fallback"
    assert result["fallback_used"] is True
    assert result["analysis"]["average_demand"] == 120
    assert result["analysis"]["forecast_demand"] == 120
    assert isinstance(result["analysis"]["recommendation"], str)
