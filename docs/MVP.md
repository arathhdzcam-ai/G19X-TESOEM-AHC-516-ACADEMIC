# MVP - SupplyChainAgentic# MVP - SupplyChainAgentic

## 1. Descripción del proyecto

SupplyChainAgentic es un proyecto académico que implementa una arquitectura basada en agentes inteligentes especializados para apoyar el análisis y la toma de decisiones en la cadena de suministro.

La solución coordina sus agentes mediante LangGraph, expone sus funcionalidades a través de FastAPI y proporciona una interfaz web mediante NiceGUI. Utiliza SQLite para persistir usuarios y resultados de análisis, y JWT para proteger las operaciones que requieren autenticación.

El propósito del MVP es demostrar cómo diferentes agentes pueden colaborar para analizar información relacionada con demanda, inventario, proveedores, abastecimiento, compras y logística.

## 2. Problema que busca resolver

La gestión de una cadena de suministro requiere analizar diferentes variables que influyen en la disponibilidad de productos, la planeación de inventarios, el desempeño de proveedores y las decisiones de compra.

Cuando estos procesos se analizan de manera aislada, puede resultar difícil consolidar la información y obtener una visión conjunta de las necesidades operativas.

SupplyChainAgentic propone una arquitectura modular en la que agentes especializados procesan los datos proporcionados por el usuario y generan resultados que facilitan el análisis de la operación.

El sistema funciona como una herramienta de apoyo a la decisión; no sustituye los sistemas transaccionales ni ejecuta operaciones reales de compra o logística.

## 3. Objetivo general

Desarrollar y validar un producto mínimo viable basado en una arquitectura Agentic que permita analizar información de demanda, inventario, proveedores, abastecimiento y logística, generar recomendaciones y conservar los resultados para su consulta posterior.

## 4. Alcance funcional del MVP

El MVP contempla las siguientes funcionalidades:

- Registro e inicio de sesión de usuarios.
- Autenticación mediante tokens JWT.
- Recepción y validación de datos de la cadena de suministro.
- Análisis de demanda histórica.
- Generación de pronóstico tradicional.
- Pronóstico de demanda asistido por IA mediante Azure OpenAI.
- Comparación de resultados de pronóstico.
- Mecanismo de respaldo determinista cuando el servicio de IA no está disponible.
- Evaluación del inventario.
- Monitoreo del desempeño de proveedores.
- Análisis de abastecimiento.
- Evaluación de necesidades de compra.
- Análisis logístico con parámetros proporcionados por el usuario.
- Orquestación de agentes mediante LangGraph.
- Exposición de operaciones mediante FastAPI.
- Interfaz de usuario mediante NiceGUI.
- Persistencia de análisis en SQLite.
- Consulta paginada del historial.
- Aislamiento de los registros por usuario autenticado.
- Pruebas automatizadas mediante pytest.

### 4.1 Parámetros proporcionados por el usuario

Además de los datos de demanda, inventario y proveedor, la solicitud de análisis permite configurar:

| Parámetro | Descripción |
|---|---|
| `lead_time_days` | Tiempo de entrega estimado en días. |
| `delay_days` | Días de retraso considerados para el análisis logístico. |
| `safety_stock` | Nivel de inventario de seguridad utilizado en el análisis de inventario y abastecimiento. |

Estos parámetros tienen valores predeterminados para mantener compatibilidad con solicitudes anteriores, pero pueden modificarse desde el formulario de NiceGUI y enviarse a través de la API.

Los valores representan información suministrada por el usuario. No constituyen datos obtenidos automáticamente de un transportista, proveedor o sistema empresarial externo.

## 5. Actores y flujo de uso

### 5.1 Actor principal: usuario

El usuario interactúa con la aplicación para proporcionar información, ejecutar análisis y consultar resultados.

Sus actividades principales son:

- Crear una cuenta.
- Iniciar sesión.
- Capturar los datos de análisis.
- Configurar los parámetros operativos.
- Ejecutar un análisis de Supply Chain.
- Consultar los resultados.
- Revisar el historial de análisis propios.

### 5.2 Flujo general

1. El usuario inicia sesión desde NiceGUI.
2. NiceGUI envía las credenciales a `POST /api/auth/login`.
3. La API valida las credenciales y devuelve un token JWT.
4. El usuario captura los datos del producto, demanda, inventario y proveedor.
5. El usuario configura el tiempo de entrega, los días de retraso y el inventario de seguridad.
6. NiceGUI envía la solicitud autenticada a FastAPI.
7. FastAPI valida los datos y obtiene la identidad del usuario.
8. LangGraph coordina los agentes correspondientes.
9. Los agentes procesan la información y generan resultados.
10. La aplicación consolida y almacena el análisis en SQLite, asociado al usuario.
11. NiceGUI presenta los resultados.
12. El usuario puede consultar su historial y los detalles de sus análisis.

## 6. Arquitectura tecnológica

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| Lenguaje | Python 3.12 | Desarrollo de la aplicación. |
| Interfaz | NiceGUI | Captura de datos y presentación de resultados. |
| API | FastAPI | Validación y exposición de servicios. |
| Modelos de datos | Pydantic | Validación de solicitudes. |
| Orquestación | LangGraph | Coordinación del flujo de agentes. |
| Componentes de IA | LangChain | Integración de componentes para modelos de lenguaje. |
| Modelo generativo | Azure OpenAI | Apoyo al pronóstico de demanda. |
| Identidad de Azure | Azure Identity | Credenciales mediante `DefaultAzureCredential`. |
| Autenticación de usuarios | JWT | Protección de las operaciones privadas. |
| Persistencia | SQLite | Usuarios e historial de análisis. |
| Pruebas | pytest | Validación automatizada. |

### 6.1 Componentes principales

- `app/main.py`: aplicación FastAPI, modelos de solicitud y endpoints de análisis e historial.
- `app/ui.py`: interfaz web NiceGUI, inicio de sesión, formulario y presentación de resultados.
- `app/auth/`: configuración, registro, inicio de sesión, seguridad y dependencias de autenticación.
- `app/core/azure_openai.py`: creación y configuración del cliente de Azure OpenAI.
- `app/orchestration/supply_chain_graph.py`: definición y ejecución del grafo de agentes.
- `app/supply_chain_database.py`: persistencia de los análisis y consultas del historial.
- `tests/`: pruebas unitarias y de integración.

## 7. Agentes implementados

La solución cuenta con agentes especializados que trabajan sobre diferentes áreas de la cadena de suministro.

| Agente | Responsabilidad | Tipo de procesamiento |
|---|---|---|
| `DemandAgent` | Analizar demanda histórica y calcular un pronóstico tradicional. | Determinista. |
| `AIDemandAgent` | Generar un pronóstico asistido por un modelo generativo. | IA generativa. |
| `InventoryAgent` | Evaluar inventario y necesidades considerando el inventario de seguridad. | Determinista. |
| `SupplierMonitoringAgent` | Evaluar indicadores de desempeño del proveedor, como entregas y calidad. | Determinista. |
| `SourcingAgent` | Analizar necesidades de abastecimiento considerando el inventario de seguridad. | Determinista. |
| `LogisticsAgent` | Analizar condiciones logísticas utilizando tiempo de entrega y días de retraso. | Determinista. |
| `PurchasingAgent` | Evaluar necesidades y generar recomendaciones de compra. | Determinista. |

### 7.1 Uso de inteligencia artificial

En la implementación actual, `AIDemandAgent` es el agente que utiliza el modelo generativo de Azure OpenAI.

Los demás agentes operan principalmente mediante reglas, cálculos y condiciones deterministas.

El flujo de pronóstico asistido por IA cuenta con un mecanismo de respaldo: si no es posible obtener el resultado del modelo, el sistema puede recurrir al pronóstico tradicional para continuar el análisis.

La incorporación de razonamiento generativo a otros agentes se considera una posible evolución, no una funcionalidad implementada en este MVP.

## 8. Orquestación mediante LangGraph

LangGraph coordina la ejecución de los agentes y permite compartir el estado del análisis.

El flujo general contempla:

1. Análisis de demanda tradicional.
2. Generación del pronóstico asistido por IA.
3. Comparación de pronósticos.
4. Evaluación de inventario.
5. Monitoreo de proveedores.
6. Análisis de abastecimiento.
7. Análisis logístico.
8. Evaluación condicional de necesidades de compra.
9. Consolidación de resultados.

Los parámetros `lead_time_days`, `delay_days` y `safety_stock` forman parte del estado compartido del grafo. De esta manera, los agentes correspondientes reciben los valores definidos en la solicitud del usuario.

La ejecución condicional permite que el flujo evalúe cuándo corresponde realizar el análisis de compras.

## 9. API y contratos principales

FastAPI proporciona los servicios que utiliza la interfaz y permite realizar solicitudes externas.

### 9.1 Rutas principales

| Método | Ruta | Función |
|---|---|---|
| `GET` | `/` | Información básica de la aplicación. |
| `GET` | `/health` | Comprobación de disponibilidad. |
| `POST` | `/api/auth/register` | Registro de usuarios. |
| `POST` | `/api/auth/login` | Inicio de sesión y emisión de token. |
| `POST` | `/api/supply-chain/analyze` | Ejecución de análisis de Supply Chain. |
| `GET` | `/api/supply-chain/history` | Consulta paginada del historial propio. |
| `GET` | `/api/supply-chain/history/{analysis_id}` | Consulta del detalle de un análisis propio. |

Las operaciones privadas requieren el token JWT correspondiente.

### 9.2 Validación de solicitudes

El modelo `DemandRequest` utiliza validaciones para controlar los datos de entrada.

Entre los parámetros operativos se encuentran:

- `lead_time_days`: entero entre 0 y 365.
- `delay_days`: entero entre 0 y 365.
- `safety_stock`: número mayor o igual a cero.

Los valores predeterminados permiten mantener compatibilidad con solicitudes que no envíen estos parámetros.

## 10. Persistencia e historial

La persistencia del MVP utiliza SQLite.

Se utilizan componentes de base de datos para almacenar la información de autenticación y los resultados de análisis.

La tabla de análisis conserva información como:

- Identificador del análisis.
- Identificador del producto.
- Identificador del proveedor, cuando corresponde.
- Fecha de creación.
- Resultado del análisis.
- Identificador del usuario propietario.

### 10.1 Aislamiento por usuario

Cada análisis nuevo queda asociado al usuario autenticado que lo generó.

Las consultas del historial filtran los registros por usuario. Asimismo, la consulta de detalle impide que un usuario recupere análisis pertenecientes a otra cuenta.

Cuando se consulta un análisis ajeno o inexistente, la API responde como recurso no encontrado, sin revelar información de otros usuarios.

La migración de bases de datos anteriores conserva los registros históricos. Los registros antiguos sin propietario no deben asignarse automáticamente a una cuenta.

## 11. Interfaz y resultados del dashboard

La interfaz está implementada con NiceGUI.

Incluye:

- Pantalla de inicio de sesión.
- Panel principal de operaciones.
- Formulario de captura de datos.
- Configuración de parámetros logísticos y de inventario.
- Presentación de pronósticos y su comparación.
- Gráficas de resultados.
- Resumen ejecutivo.
- Alertas y tarjetas operativas.
- Historial de análisis.
- Consulta del detalle de resultados.
- Cierre de sesión.

El acceso a los datos se realiza mediante la API y el token de autenticación del usuario.

La carpeta `frontend/` conserva una plantilla inicial de Vite. No representa una interfaz React integrada al MVP; la interfaz funcional actual es NiceGUI.

## 12. Requisitos de ejecución y configuración

Para ejecutar el MVP se necesita:

- Windows y Python 3.12.
- Dependencias instaladas desde `requirements.txt`.
- Archivo `.env` configurado.
- Secreto JWT de al menos 32 caracteres.
- Endpoint y despliegue de Azure OpenAI cuando se requiera pronóstico mediante IA.
- Credencial válida para `DefaultAzureCredential`.

La aplicación se ejecuta mediante dos procesos:

**API:**

```powershell
python -m uvicorn app.main:app --reload
```

**Interfaz:**

```powershell
python -m app.ui
```

La documentación de FastAPI se encuentra en `http://127.0.0.1:8000/docs` y la interfaz NiceGUI en `http://127.0.0.1:8080`.

## 13. Criterios de aceptación

El MVP se considera funcional cuando se cumplen los siguientes criterios verificables:

- El usuario puede registrarse e iniciar sesión.
- NiceGUI utiliza el endpoint de autenticación de la API.
- Los endpoints privados requieren autenticación.
- La API valida los datos de entrada.
- El análisis se ejecuta mediante el grafo de LangGraph.
- El pronóstico tradicional puede servir como respaldo cuando falla la IA.
- El inventario utiliza el inventario de seguridad proporcionado.
- El abastecimiento utiliza el inventario de seguridad proporcionado.
- La logística utiliza el tiempo de entrega y los días de retraso proporcionados.
- Los análisis se almacenan en SQLite.
- El historial permite paginación.
- Un usuario no puede consultar los análisis de otro usuario.
- La interfaz presenta los resultados y permite consultar el historial.
- Las pruebas automatizadas correspondientes terminan sin fallos.
- La documentación representa el estado real del código.

## 14. Limitaciones actuales

El MVP tiene las siguientes limitaciones:

- La calidad de los resultados depende de los datos proporcionados por el usuario.
- El pronóstico generativo depende de la disponibilidad, configuración y permisos de Azure OpenAI.
- Los agentes distintos de `AIDemandAgent` utilizan principalmente reglas y cálculos deterministas.
- Los parámetros logísticos son suministrados por el usuario; no se obtienen automáticamente de transportistas.
- No existe una conexión transaccional con ERP, WMS, TMS o sistemas de proveedores.
- Las recomendaciones de compra no generan órdenes reales.
- SQLite está orientado al entorno local del MVP y no constituye por sí mismo una solución de persistencia empresarial distribuida.
- La carpeta `frontend/` no está integrada como una aplicación React funcional.

## 15. Funcionalidades fuera del alcance confirmado

No se consideran implementadas por el simple hecho de formar parte de la arquitectura objetivo:

- Persistencia empresarial con PostgreSQL.
- Caché o mensajería distribuida con Redis.
- Recuperación documental con Azure AI Search.
- Despliegue mediante Docker y Kubernetes.
- Integración de indicadores con Power BI.
- Automatización CI/CD mediante GitHub Actions.
- Interfaz React integrada como sustitución de NiceGUI.
- Conexiones automáticas con sistemas empresariales externos.
- Ejecución real de órdenes de compra.
- Razonamiento generativo en todos los agentes.

Estas capacidades requieren diseño, implementación y validación independientes.

## 16. Evolución futura

Como líneas de evolución se consideran:

1. Evaluar la incorporación de razonamiento asistido por IA a un segundo agente, manteniendo un mecanismo determinista de respaldo.
2. Incorporar observabilidad, métricas y trazabilidad del flujo de agentes.
3. Evaluar PostgreSQL para escenarios con mayores necesidades de persistencia.
4. Incorporar integraciones empresariales cuando exista una necesidad funcional concreta.
5. Evaluar Docker y automatización de pruebas mediante CI/CD.
6. Ampliar los indicadores y herramientas de análisis.
7. Evaluar una transición de interfaz únicamente cuando se haya definido cómo conservar las funcionalidades existentes.

Cada evolución deberá contar con criterios de aceptación y pruebas antes de considerarse implementada.

## 17. Validación automatizada

La última ejecución completa registrada de la suite de pruebas fue:

`58 passed in 47.90s`

La ejecución se realizó el 10 de noviembre de 2026 mediante el entorno virtual del proyecto.

Este resultado corresponde a la versión validada en esa fecha. Cualquier cambio posterior en el código o en las pruebas requiere una nueva ejecución para actualizar la evidencia.

Comando utilizado:

```powershell
python -m pytest -v
```

## 18. Declaración sobre asistencia de IA

Durante el desarrollo y la documentación del proyecto se utilizó un asistente de inteligencia artificial como apoyo para tareas de escritura, revisión y mejora del código.

El desarrollador revisa y valida los resultados mediante inspección del código, pruebas automatizadas y comprobaciones de funcionamiento. La responsabilidad de la integración y validación final corresponde al desarrollador.