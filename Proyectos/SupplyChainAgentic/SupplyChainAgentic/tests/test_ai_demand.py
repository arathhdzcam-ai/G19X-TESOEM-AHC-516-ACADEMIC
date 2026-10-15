
from app.agents.ai_demand_agent import AIDemandAgent


def test_ai_demand_returns_analysis():
    agent = AIDemandAgent()

    result = agent.analyze(
        historical_demand=[100, 120, 110, 130, 140]
    )

    assert isinstance(result, dict)
    assert "analysis" in result
    assert isinstance(result["analysis"], dict)
    assert "recommendation" in result["analysis"]