
from contextlib import asynccontextmanager
from pathlib import Path
from html import escape

import jwt
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.auth.database import initialize_database, get_db_connection
from app.supply_chain_database import (
    initialize_supply_chain_database,
    save_supply_chain_analysis,
)


from app.auth.dependencies import get_current_user
from app.auth.routes import router as auth_router
from app.auth.security import (
    verify_password,
    create_access_token,
    decode_access_token,
)

from app.orchestration.supply_chain_graph import build_supply_chain_graph


# Inicialización de la base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    initialize_supply_chain_database()
    yield

# Aplicación FastAPI
app = FastAPI(
    title="Supply Chain Agentic API",
    description="API para la arquitectura Agentic de Supply Chain",
    version="1.0.0",
    lifespan=lifespan,
)

# Rutas de autenticación que ya existían
app.include_router(auth_router)


# Configuración de HTML y archivos estáticos
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# Modelo de entrada para el análisis de Supply Chain
class DemandRequest(BaseModel):
    product_id: str = Field(min_length=1, max_length=100)
    historical_demand: list[float] = Field(min_length=1, max_length=1000)
    forecast_periods: int = Field(default=3, ge=1, le=36)
    current_inventory: float = Field(ge=0)
    supplier_id: str = Field(min_length=1, max_length=100)
    on_time_delivery_rate: float = Field(ge=0, le=1)
    quality_rate: float = Field(ge=0, le=1)
    supplier_capacity: float = Field(ge=0)


# Página principal de la API
@app.get("/")
def root():
    return {
        "application": "Supply Chain Agentic",
        "status": "online",
        "message": "API funcionando correctamente",
        "login": "/login",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# Mostrar el formulario de inicio de sesión
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None},
    )


# Procesar las credenciales del formulario
@app.post("/login")
def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    email = email.strip().lower()

    with get_db_connection() as connection:
        user = connection.execute(
            """
            SELECT id, email, password_hash, is_active
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    # Mensaje genérico para credenciales incorrectas
    if (
        user is None
        or not verify_password(password, user["password_hash"])
        or not user["is_active"]
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Correo o contraseña incorrectos, o cuenta desactivada."
            },
            status_code=401,
        )

    # Crear un JWT utilizando el sistema de autenticación existente
    token = create_access_token(
        user_id=user["id"],
        email=user["email"],
    )

    response = RedirectResponse(
        url="/dashboard",
        status_code=303,
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800,
        path="/",
    )

    return response


# Panel protegido: requiere una sesión válida
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])

    except (
        jwt.InvalidTokenError,
        ValueError,
        KeyError,
        TypeError,
    ):
        response = RedirectResponse(
            url="/login",
            status_code=303,
        )
        response.delete_cookie("access_token", path="/")
        return response

    # Comprobar que la cuenta siga existiendo y activa
    with get_db_connection() as connection:
        user = connection.execute(
            """
            SELECT id, email, is_active
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    if user is None or not user["is_active"]:
        response = RedirectResponse(
            url="/login",
            status_code=303,
        )
        response.delete_cookie("access_token", path="/")
        return response

    safe_email = escape(user["email"])

    return HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1">
            <title>SupplyChainAgentic | Panel principal</title>
            <style>
                body {{
                    margin: 0;
                    padding: 40px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    background: #f5f7fb;
                    color: #17243a;
                }}
                main {{
                    max-width: 850px;
                    margin: 50px auto;
                    padding: 35px;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 8px 35px #17243a12;
                }}
                h1 {{ color: #126d78; }}
                .logout {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 18px;
                    background: #126d78;
                    color: white;
                    border-radius: 8px;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <main>
                <h1>SupplyChainAgentic</h1>
                <h2>Bienvenido al panel principal</h2>
                <p>Sesión iniciada como:
                   <strong>{safe_email}</strong></p>
                <p>Tu acceso a la plataforma ha sido validado.</p>
                <a class="logout" href="/logout">Cerrar sesión</a>
            </main>
        </body>
        </html>
        """
    )


# Cerrar la sesión
@app.get("/logout")
def logout():
    response = RedirectResponse(
        url="/login",
        status_code=303,
    )
    response.delete_cookie("access_token", path="/")
    return response


# Análisis de Supply Chain: conserva la protección existente
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

        analysis_id = save_supply_chain_analysis(response)

        return {
            **response,
            "analysis_id": analysis_id,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
