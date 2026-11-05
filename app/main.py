
from contextlib import asynccontextmanager



from fastapi import Depends, FastAPI, HTTPException

from pydantic import BaseModel, Field, field_validator

from app.auth.database import initialize_database
from app.supply_chain_database import (
    initialize_supply_chain_database,
    save_supply_chain_analysis,
    get_supply_chain_analysis,
    list_supply_chain_analyses,
)


from app.auth.dependencies import get_current_user
from app.auth.routes import router as auth_router


from app.orchestration.supply_chain_graph import build_supply_chain_graph


# Inicializacion de la base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    initialize_supply_chain_database()
    yield

# Aplicacion FastAPI
app = FastAPI(
    title="Supply Chain Agentic API",
    description="API para la arquitectura Agentic de Supply Chain",
    version="1.0.0",
    lifespan=lifespan,
)

# Rutas de autenticacion que ya existi­an
app.include_router(auth_router)




# Modelo de entrada para el analisis de Supply Chain
class DemandRequest(BaseModel):
    product_id: str = Field(min_length=1, max_length=100)
    historical_demand: list[float] = Field(min_length=1, max_length=1000)
    forecast_periods: int = Field(default=3, ge=1, le=36)
    current_inventory: float = Field(ge=0)
    supplier_id: str = Field(min_length=1, max_length=100)
    on_time_delivery_rate: float = Field(ge=0, le=1)
    quality_rate: float = Field(ge=0, le=1)
    supplier_capacity: float = Field(ge=0)
    lead_time_days: int = Field(default=5, ge=0, le=365)
    delay_days: int = Field(default=0, ge=0, le=365)
    safety_stock: float = Field(default=20, ge=0)

    @field_validator("product_id", "supplier_id")
    @classmethod
    def validate_identifiers(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El identificador es obligatorio.")

        if value.casefold() == "string":
            raise ValueError(
                "Reemplaza el valor de ejemplo 'string' por un identificador real."
            )

        return value

# Pagina principal de la API
@app.get("/")
def root():
    return {
        "application": "Supply Chain Agentic",
        "status": "online",
        "message": "API funcionando correctamente",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

# Analisis de Supply Chain: conserva la proteccion existente

@app.post("/api/supply-chain/analyze")
def analyze_supply_chain(
    request: DemandRequest,
    current_user: dict = Depends(get_current_user),
):
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
            "lead_time_days": request.lead_time_days,
            "delay_days": request.delay_days,
            "safety_stock": request.safety_stock,
            "supplier_result": {},
            "demand_result": {},
            "ai_demand_result": {},
            "forecast_comparison": {},
            "inventory_result": {},
            "purchasing_result": {},
            "sourcing_result": {},
                        "logistics_result": {},
        }

        result = graph.invoke(initial_state)

        response = {
            "product_id": result["product_id"],
            "demand_analysis": result["demand_result"],
            "ai_demand_analysis": result["ai_demand_result"],
            "forecast_comparison": result["forecast_comparison"],
            "inventory_analysis": result["inventory_result"],
            "supplier_analysis": result["supplier_result"],
            "sourcing_analysis": result.get("sourcing_result", {}),
            "logistics_analysis": result.get("logistics_result", {}),
            "purchasing_analysis": result["purchasing_result"],
        }

        # Guardar el analisis en la base de datos.

        analysis_id = save_supply_chain_analysis(
            response,
            user_id=current_user["id"],
        )
        # Devolver el resultado junto con su identificador.
        return {
            **response,
            "analysis_id": analysis_id,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


# Consultar el historial de analisis de Supply Chain.

@app.get("/api/supply-chain/history")
def get_supply_chain_history(
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
):
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=422,
            detail="limit debe estar entre 1 y 100.",
        )

    if offset < 0:
        raise HTTPException(
            status_code=422,
            detail="offset no puede ser negativo.",
        )

    analyses = list_supply_chain_analyses(
        user_id=current_user["id"],
        limit=limit,
        offset=offset,
    )

    return {
        "items": analyses,
        "limit": limit,
        "offset": offset,
        "count": len(analyses),
    }




# Consultar un analisis especifico por su identificador.
@app.get("/api/supply-chain/history/{analysis_id}")
def get_supply_chain_analysis_by_id(
    analysis_id: int,
    current_user: dict = Depends(get_current_user),
):
    if analysis_id < 1:
        raise HTTPException(
            status_code=422,
            detail="analysis_id debe ser un entero positivo.",
        )


    analysis = get_supply_chain_analysis(
        analysis_id,
        user_id=current_user["id"],
    )


    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el análisis solicitado.",
        )

    return analysis
