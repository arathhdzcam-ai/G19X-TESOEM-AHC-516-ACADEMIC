
from nicegui import app as nicegui_app, ui

from app.auth.config import JWT_SECRET_KEY
from app.auth.database import get_db_connection
from app.auth.security import verify_password, create_access_token

import httpx
from nicegui import run



# Configuración visual temporalmente desactivada
# ui.colors(
#     primary="#126d78",
#     secondary="#168b91",
#     accent="#79d5d0",
# )




nicegui_app.add_static_files(
    "/static",
    "app/static",
)


@ui.page("/")
def index():
    if nicegui_app.storage.user.get("email"):
        ui.navigate.to("/dashboard")
    else:
        ui.navigate.to("/login")


@ui.page("/login")
def login_page():
    ui.query("body").style("background-color: #f5f7fb")

    with ui.column().classes(
        "w-full min-h-screen items-center justify-center p-4"
    ):
        with ui.card().classes("w-full max-w-md p-8 rounded-xl"):
            with ui.column().classes("w-full items-center gap-1"):
                ui.label("SC").classes(
                    "text-3xl font-bold text-primary"
                )
                ui.label("SUPPLYCHAINAGENTIC").classes(
                    "text-lg font-bold"
                )
                ui.label("Plataforma inteligente de Supply Chain").classes(
                    "text-sm text-gray-500 text-center"
                )

            ui.separator().classes("my-4")

            ui.label("Bienvenido de nuevo").classes(
                "text-2xl font-bold"
            )
            ui.label("Ingresa tus credenciales para continuar.").classes(
                "text-gray-500 text-sm"
            )

            email_input = ui.input(
                "Correo electrónico",
                placeholder="nombre@empresa.com",
            ).classes("w-full")

            password_input = ui.input(
                "Contraseña",
                password=True,
                password_toggle_button=True,
            ).classes("w-full")

            error_label = ui.label("").classes("text-red-600 text-sm")

            def login():
                email = (email_input.value or "").strip().lower()
                password = password_input.value or ""

                if not email or not password:
                    error_label.set_text(
                        "Ingresa tu correo y contraseña."
                    )
                    return

                with get_db_connection() as connection:
                    user = connection.execute(
                        """
                        SELECT id, email, password_hash, is_active
                        FROM users
                        WHERE email = ?
                        """,
                        (email,),
                    ).fetchone()

                if (
                    user is None
                    or not verify_password(
                        password,
                        user["password_hash"] if user else "",
                    )
                    or not user["is_active"]
                ):
                    error_label.set_text(
                        "Correo o contraseña incorrectos."
                    )
                    return


                token = create_access_token(
                    user_id=user["id"],
                    email=user["email"],
                )

                nicegui_app.storage.user["user_id"] = user["id"]
                nicegui_app.storage.user["email"] = user["email"]
                nicegui_app.storage.user["access_token"] = token

                ui.navigate.to("/dashboard")


            ui.button(
                "Iniciar sesión",
                on_click=login,
            ).classes("w-full mt-4")

            ui.label(
                "Acceso protegido · SupplyChainAgentic"
            ).classes("w-full text-center text-xs text-gray-400 mt-4")


@ui.page("/dashboard")
def dashboard_page():
    email = nicegui_app.storage.user.get("email")
    user_id = nicegui_app.storage.user.get("user_id")

    if not email or not user_id:
        ui.navigate.to("/login")
        return


    with ui.header().classes(
        "w-full items-center justify-between px-6"
    ).style("background-color: #142b45; color: white;"):
        with ui.row().classes("items-center gap-3"):
            ui.label("SC").classes("text-2xl font-bold")
            ui.label("SupplyChainAgentic").classes(
                "text-lg font-bold"
            )

        with ui.row().classes("items-center gap-3"):
            ui.label(email).classes("text-sm")

            def logout():
                nicegui_app.storage.user.pop("user_id", None)
                nicegui_app.storage.user.pop("email", None)
                nicegui_app.storage.user.pop("access_token", None)
                ui.navigate.to("/login")

            ui.button(
                "Cerrar sesión",
                on_click=logout,
                icon="logout",
            ).props("outline color=white").classes(
                "font-bold"
            )


    with ui.column().classes(
        "w-full max-w-7xl mx-auto p-6 gap-6"
    ):
        ui.label("CENTRO DE OPERACIONES").classes(
            "text-xs font-bold tracking-widest text-primary"
        )

        ui.label("Panel principal").classes(
            "text-3xl font-bold"
        )

        ui.label(
            "Monitorea y analiza tu cadena de suministro."
        ).classes("text-gray-500")

        with ui.card().classes(
            "w-full p-6 text-white rounded-xl"
        ).style(
            "background: linear-gradient(115deg, #142b45, #176d78)"
        ):
            ui.label(
                "Bienvenido a SupplyChainAgentic"
            ).classes("text-2xl font-bold")

            ui.label(
                "Coordina agentes inteligentes para apoyar "
                "las decisiones de demanda, inventario, compras "
                "y proveedores."
            ).classes("text-base")

        ui.label("Módulos de la plataforma").classes(
            "text-xl font-bold"
        )

        with ui.grid(columns=2).classes("w-full gap-4"):
            with ui.card().classes("w-full p-4"):
                ui.icon("trending_up", size="2rem").classes(
                    "text-primary"
                )
                ui.label("Pronóstico de demanda").classes(
                    "text-lg font-bold"
                )
                ui.label(
                    "Proyecciones basadas en la demanda histórica."
                ).classes("text-sm text-gray-500")

            with ui.card().classes("w-full p-4"):
                ui.icon("inventory_2", size="2rem").classes(
                    "text-primary"
                )
                ui.label("Gestión de inventarios").classes(
                    "text-lg font-bold"
                )
                ui.label(
                    "Evaluación de existencias y necesidades."
                ).classes("text-sm text-gray-500")

            with ui.card().classes("w-full p-4"):
                ui.icon("local_shipping", size="2rem").classes(
                    "text-primary"
                )
                ui.label("Monitoreo de proveedores").classes(
                    "text-lg font-bold"
                )
                ui.label(
                    "Indicadores de calidad, entregas y capacidad."
                ).classes("text-sm text-gray-500")

            with ui.card().classes("w-full p-4"):
                ui.icon("shopping_cart", size="2rem").classes(
                    "text-primary"
                )
                ui.label("Compras y abastecimiento").classes(
                    "text-lg font-bold"
                )
                ui.label(
                    "Apoyo a las decisiones de abastecimiento."
                ).classes("text-sm text-gray-500")

        with ui.card().classes("w-full p-4"):
            ui.label(
                "Capa de orquestación inteligente"
            ).classes("text-lg font-bold")
            ui.label(
                "Los agentes se coordinan mediante LangGraph. "
                "En el siguiente paso conectaremos este panel "
                "con el análisis real de Supply Chain."
            ).classes("text-sm text-gray-600")


        ui.label("Análisis de Supply Chain").classes(
            "text-xl font-bold mt-6"
        )

        with ui.card().classes("w-full p-6 gap-4"):
            product_input = ui.input(
                "ID del producto",
                value="SKU-001",
            ).classes("w-full")

            history_input = ui.input(
                "Demanda histórica (separada por comas)",
                value="100,120,110,130,140",
            ).classes("w-full")

            periods_input = ui.number(
                "Periodos de pronóstico",
                value=3,
                min=1,
                max=36,
                precision=0,
            ).classes("w-full")

            inventory_input = ui.number(
                "Inventario actual",
                value=100,
                min=0,
            ).classes("w-full")

            supplier_input = ui.input(
                "ID del proveedor",
                value="SUP-001",
            ).classes("w-full")

            delivery_input = ui.number(
                "Tasa de entregas a tiempo (0 a 1)",
                value=0.95,
                min=0,
                max=1,
            ).classes("w-full")

            quality_input = ui.number(
                "Tasa de calidad (0 a 1)",
                value=0.98,
                min=0,
                max=1,
            ).classes("w-full")

            capacity_input = ui.number(
                "Capacidad del proveedor",
                value=200,
                min=0,
            ).classes("w-full")

            status_label = ui.label("")
            result_area = ui.column().classes("w-full gap-3")

            async def execute_analysis():
                status_label.set_text("Ejecutando análisis...")
                result_area.clear()

                try:
                    historical = [
                        float(value.strip())
                        for value in history_input.value.split(",")
                        if value.strip()
                    ]

                    if not historical:
                        raise ValueError(
                            "Ingresa al menos un valor de demanda histórica."
                        )

                    if not product_input.value.strip():
                        raise ValueError("Ingresa el ID del producto.")

                    if not supplier_input.value.strip():
                        raise ValueError("Ingresa el ID del proveedor.")

                    if periods_input.value is None or not 1 <= periods_input.value <= 36:
                        raise ValueError(
                            "Los periodos deben estar entre 1 y 36."
                        )

                    payload = {
                        "product_id": product_input.value.strip(),
                        "historical_demand": historical,
                        "forecast_periods": int(periods_input.value),
                        "current_inventory": float(inventory_input.value or 0),
                        "supplier_id": supplier_input.value.strip(),
                        "on_time_delivery_rate": float(delivery_input.value),
                        "quality_rate": float(quality_input.value),
                        "supplier_capacity": float(capacity_input.value or 0),
                    }

                    token = nicegui_app.storage.user.get("access_token")

                    if not token:
                        status_label.set_text(
                            "La sesión no tiene token. Cierra sesión e inicia de nuevo."
                        )
                        return

                    response = await run.io_bound(
                        httpx.post,
                        "http://127.0.0.1:8000/api/supply-chain/analyze",
                        json=payload,
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=60.0,
                    )

                    if response.status_code == 401:
                        status_label.set_text(
                            "Sesión expirada o no autorizada. "
                            "Cierra sesión e inicia de nuevo."
                        )
                        return

                    response.raise_for_status()
                    data = response.json()

                    status_label.set_text("Análisis completado correctamente.")

                    with result_area:
                        ui.label(
                            f"Producto: {data['product_id']}"
                        ).classes("text-lg font-bold")

                        for title, key in [
                            ("Pronóstico de demanda", "demand_analysis"),
                            ("Análisis de demanda con IA", "ai_demand_analysis"),
                            ("Comparación de pronósticos", "forecast_comparison"),
                            ("Análisis de inventario", "inventory_analysis"),
                            ("Análisis de proveedores", "supplier_analysis"),
                            ("Compras y abastecimiento", "purchasing_analysis"),
                        ]:
                            with ui.expansion(title).classes("w-full"):
                                ui.json_editor({
                                    "content": {
                                        "json": data.get(key, {})
                                    }
                                }).classes("w-full")

                except ValueError as error:
                    status_label.set_text(str(error))
                except httpx.HTTPStatusError as error:
                    try:
                        detail = error.response.json().get(
                            "detail",
                            error.response.text,
                        )
                    except ValueError:
                        detail = error.response.text

                    status_label.set_text(
                        f"Error de la API ({error.response.status_code}): {detail}"
                    )
                except httpx.RequestError:
                    status_label.set_text(
                        "No se pudo conectar con FastAPI. "
                        "Comprueba que el servidor del puerto 8000 esté activo."
                    )
                except Exception as error:
                    status_label.set_text(
                        f"Error durante el análisis: {error}"
                    )

            ui.button(
                "Ejecutar análisis",
                on_click=execute_analysis,
                icon="play_arrow",
            ).classes("w-full")





# Configuración visual desactivada temporalmente
# ui.colors(
#     primary="#126d78",
#     secondary="#168b91",
#     accent="#79d5d0",
# )


if __name__ == "__main__":
    ui.run(
        title="SupplyChainAgentic",
        host="127.0.0.1",
        port=8080,
        storage_secret=JWT_SECRET_KEY,
        reload=False,
    )
