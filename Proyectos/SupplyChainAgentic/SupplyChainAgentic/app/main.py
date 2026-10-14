from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.orchestration.supply_chain_graph import build_supply_chain_graph


app = FastAPI(
    title="Supply Chain Agentic API",
    description="API para la arquitectura Agentic de Supply Chain",
    version="1.0.0")


class DemandRequest(BaseModel):
    product_id: str
    historical_demand: list[float]
    forecast_periods: int = 3
    current_inventory: float
    supplier_id: str
    on_time_delivery_rate: float
    quality_rate: float
    supplier_capacity: float


@app.get("/")
def root():
    return {
        "application": "Supply Chain Agentic",
        "status": "online",
        "message": "API funcionando correctamente"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/supply-chain/analyze")

def analyze_supply_chain(request: DemandRequest):
    try:
        graph = build_supply_chain_graph()

        initial_state = {
            "product_id": request.product_id,
            "historical_demand": request.historical_demand,
            "forecast_periods": request.forecast_periods,
            "current_inventory": request.current_inventory,
            "supplier_id": request.supplier_id,
            "on_time_delivery_rate": request.on_time_delivery_rate,
            "quality_rate": request.quality_rate,
            "supplier_capacity": request.supplier_capacity,
            "supplier_result": {},
            "demand_result": {},
            "ai_demand_result": {},
            "forecast_comparison": {},
            "inventory_result": {},
            "purchasing_result": {}
        }

  
        result = graph.invoke(initial_state)

        return {
            "product_id": result["product_id"],
            "demand_analysis": result["demand_result"],
            "ai_demand_analysis": result["ai_demand_result"],
            "forecast_comparison": result["forecast_comparison"],
            "inventory_analysis": result["inventory_result"],
            "supplier_analysis": result["supplier_result"],
            "purchasing_analysis": result["purchasing_result"]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error))
    