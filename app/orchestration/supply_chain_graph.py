
from typing import TypedDict
import math

from langgraph.graph import StateGraph, START, END

from app.agents.demand_agent import DemandAgent
from app.agents.inventory_agent import InventoryAgent
from app.agents.purchasing_agent import PurchasingAgent
from app.agents.ai_demand_agent import AIDemandAgent
from app.agents.supplier_monitoring_agent import SupplierMonitoringAgent
from app.agents.sourcing_agent import SourcingAgent
from app.agents.logistics_agent import LogisticsAgent


class SupplyChainState(TypedDict):
    historical_demand: list[float]
    forecast_periods: int
    current_inventory: float
    product_id: str
    supplier_id: str
    on_time_delivery_rate: float
    quality_rate: float
    supplier_capacity: float
    supplier_result: dict
    demand_result: dict
    ai_demand_result: dict
    forecast_comparison: dict
    inventory_result: dict
    purchasing_result: dict
    sourcing_result: dict
    logistics_result: dict




def get_safe_ai_forecast(state: SupplyChainState) -> float:
    """Obtiene el pronóstico de IA o usa el tradicional como respaldo."""

    ai_result = state.get("ai_demand_result") or {}
    analysis = ai_result.get("analysis") or {}
    forecast = analysis.get("forecast_demand")

    if (
        isinstance(forecast, (int, float))
        and not isinstance(forecast, bool)
        and math.isfinite(forecast)
        and forecast >= 0
    ):
        return float(forecast)

    # Respaldo: pronóstico tradicional de DemandAgent.
    demand_result = state.get("demand_result") or {}
    traditional_forecasts = demand_result.get("forecast") or []

    if traditional_forecasts:
        fallback = traditional_forecasts[0]
    else:
        fallback = demand_result.get("average_demand")

    if (
        isinstance(fallback, (int, float))
        and not isinstance(fallback, bool)
        and math.isfinite(fallback)
        and fallback >= 0
    ):
        return float(fallback)

    raise ValueError(
        "No existe un pronóstico válido de IA ni un pronóstico "
        "tradicional para continuar el análisis."
    )



def analyze_supplier(state: SupplyChainState) -> SupplyChainState:
    agent = SupplierMonitoringAgent()

    result = agent.analyze(
        supplier_id=state["supplier_id"],
        on_time_delivery_rate=state["on_time_delivery_rate"],
        quality_rate=state["quality_rate"],
        capacity=state["supplier_capacity"],
    )

    return {**state, "supplier_result": result}


def analyze_demand(state: SupplyChainState) -> SupplyChainState:
    agent = DemandAgent(forecast_periods=state["forecast_periods"])

    result = agent.forecast(
        historical_demand=state["historical_demand"]
    )

    return {**state, "demand_result": result}


def analyze_ai_demand(state: SupplyChainState) -> SupplyChainState:
    agent = AIDemandAgent()

    result = agent.analyze(
        historical_demand=state["historical_demand"]
    )

    return {**state, "ai_demand_result": result}



def compare_forecasts(state: SupplyChainState) -> SupplyChainState:
    traditional_forecast = state["demand_result"]["forecast"][0]
    ai_forecast = get_safe_ai_forecast(state)

    return {
        **state,
        "forecast_comparison": {
            "traditional_forecast": traditional_forecast,
            "ai_forecast": ai_forecast,
            "difference": ai_forecast - traditional_forecast,
        },
    }




def analyze_inventory(state: SupplyChainState) -> SupplyChainState:
    forecast_demand = get_safe_ai_forecast(state)

    agent = InventoryAgent(safety_stock=20)
    result = agent.analyze(
        current_inventory=state["current_inventory"],
        forecast_demand=forecast_demand,
    )

    return {**state, "inventory_result": result}




def analyze_sourcing(state: SupplyChainState) -> SupplyChainState:
    forecast_demand = get_safe_ai_forecast(state)

    agent = SourcingAgent()
    result = agent.analyze(
        product_id=state["product_id"],
        forecast_demand=forecast_demand,
        current_inventory=state["current_inventory"],
        safety_stock=20,
        supplier_capacity=state["supplier_capacity"],
    )

    return {**state, "sourcing_result": result}



def analyze_logistics(state: SupplyChainState) -> SupplyChainState:
    agent = LogisticsAgent()
    result = agent.analyze(
        on_time_delivery_rate=state["on_time_delivery_rate"],
        lead_time_days=5,
        delay_days=0,
    )

    return {**state, "logistics_result": result}



def analyze_purchasing(state: SupplyChainState) -> SupplyChainState:
    sourcing_result = state["sourcing_result"]

    # Usar la cantidad que abastecimiento puede suministrar.
    recommended_order = sourcing_result["recommended_quantity"]

    agent = PurchasingAgent()
    result = agent.recommend_purchase(
        product_id=state["product_id"],
        quantity=recommended_order,
    )

    # Conservar la información del abastecimiento
    # para poder identificar faltantes pendientes.
    result["unmet_quantity"] = sourcing_result["unmet_quantity"]

    return {**state, "purchasing_result": result}



def should_purchase(state: SupplyChainState) -> str:
    inventory_status = state["inventory_result"]["inventory_status"]

    if inventory_status == "low":
        return "analyze_purchasing"

    return "end"


def build_supply_chain_graph():
    graph = StateGraph(SupplyChainState)

    graph.add_node("analyze_demand", analyze_demand)
    graph.add_node("analyze_ai_demand", analyze_ai_demand)
    graph.add_node("compare_forecasts", compare_forecasts)
    graph.add_node("analyze_inventory", analyze_inventory)
    graph.add_node("analyze_supplier", analyze_supplier)
    graph.add_node("analyze_sourcing", analyze_sourcing)
    graph.add_node("analyze_logistics", analyze_logistics)
    graph.add_node("analyze_purchasing", analyze_purchasing)

    graph.add_edge(START, "analyze_demand")
    graph.add_edge("analyze_demand", "analyze_ai_demand")
    graph.add_edge("analyze_ai_demand", "compare_forecasts")
    graph.add_edge("compare_forecasts", "analyze_inventory")
    graph.add_edge("analyze_inventory", "analyze_supplier")
    graph.add_edge("analyze_supplier", "analyze_sourcing")
    graph.add_edge("analyze_sourcing", "analyze_logistics")

    graph.add_conditional_edges(
        "analyze_logistics",
        should_purchase,
        {
            "analyze_purchasing": "analyze_purchasing",
            "end": END,
        },
    )

    graph.add_edge("analyze_purchasing", END)

    return graph.compile()
