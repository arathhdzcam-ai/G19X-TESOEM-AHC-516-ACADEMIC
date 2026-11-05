from app.agents.ai_demand_agent import AIDemandAgent

agent = AIDemandAgent()

result = agent.analyze(
    historical_demand=[100, 120, 110, 130, 140]
)

print("\n=== ANALISIS DE DEMANDA ===")
print(result["analysis"])
