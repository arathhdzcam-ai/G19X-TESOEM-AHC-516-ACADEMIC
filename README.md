# SupplyChainAgentic

**Arquitectura Agentic para la gestión inteligente de Supply Chain**

## 1. Descripción del proyecto

SupplyChainAgentic es una aplicación académica que implementa una arquitectura basada en agentes inteligentes especializados para apoyar el análisis y la toma de decisiones en la cadena de suministro.

Los agentes se coordinan mediante LangGraph. Sus funcionalidades se exponen a través de una API desarrollada con FastAPI y una interfaz web construida con NiceGUI.

### Objetivo general

Desarrollar una arquitectura Agentic para optimizar integralmente la cadena de suministro mediante agentes especializados, integración de inteligencia artificial, automatización y persistencia de información.

### Funcionalidades principales

- Análisis de demanda histórica y generación de pronósticos.
- Pronóstico asistido por IA y comparación con el pronóstico tradicional.
- Mecanismo de respaldo determinista cuando el servicio de IA no está disponible.
- Análisis de inventario e inventario de seguridad configurable.
- Monitoreo y evaluación de proveedores.
- Análisis de abastecimiento y necesidades de compra.
- Análisis logístico con tiempo de entrega y días de retraso configurables.
- Orquestación de agentes mediante LangGraph.
- API REST con FastAPI.
- Interfaz web con NiceGUI.
- Autenticación mediante JWT.
- Historial de análisis persistido y aislado por usuario.

## 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python 3.12 | Lenguaje principal |
| FastAPI | API y servicios del sistema |
| LangGraph | Orquestación de agentes |
| LangChain | Componentes para aplicaciones con modelos de lenguaje |
| Azure OpenAI | Pronóstico de demanda asistido por IA |
| Azure Identity | Obtención de credenciales mediante `DefaultAzureCredential` |
| Microsoft Entra ID | Identidad utilizada para acceder a Azure |
| NiceGUI | Interfaz web |
| SQLite | Persistencia de usuarios e historial de análisis |
| Pydantic | Validación de datos |
| PyJWT | Gestión de tokens JWT |
| pytest | Pruebas automatizadas |
| Git y GitHub | Control de versiones |

## 3. Requisitos previos

- Windows 10 u 11.
- Python 3.12.
- Git.
- Visual Studio con herramientas de desarrollo de Python.
- Acceso al repositorio.
- Una cuenta de Azure con acceso al recurso de Azure OpenAI, si se utilizará el pronóstico mediante IA.
- Una credencial compatible con `DefaultAzureCredential`.

La aplicación se ejecuta localmente. Las solicitudes que utilizan Azure OpenAI requieren acceso al servicio y pueden consumir cuota o generar cargos según la suscripción y sus condiciones.

## 4. Obtener el código fuente

Abre PowerShell o la terminal de Visual Studio:

```powershell
git clone https://github.com/arathhdzcam-ai/G19X-TESOEM-AHC-516-ACADEMIC.git
```

Entra en la carpeta del repositorio:

```powershell
cd G19X-TESOEM-AHC-516-ACADEMIC
```

Comprueba que estás en la raíz del proyecto, donde se encuentran `README.md`, `requirements.txt` y la carpeta `app`.

## 5. Crear el entorno virtual

Desde la raíz del proyecto:

```powershell
py -3.12 -m venv .venv
```

Activa el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Comprueba la versión:

```powershell
python --version
```

Comprueba el intérprete utilizado:

```powershell
python -c "import sys; print(sys.executable)"
```

La ruta debe corresponder a `.venv\Scripts\python.exe`.

Si PowerShell impide activar el entorno, puedes permitirlo temporalmente en la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después vuelve a ejecutar el comando de activación.

## 6. Instalar las dependencias

Actualiza pip:

```powershell
python -m pip install --upgrade pip
```

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Comprueba los conflictos conocidos:

```powershell
python -m pip check
```

## 7. Configurar las variables de entorno

El proyecto utiliza variables de entorno para separar la configuración y las credenciales del código fuente.

En la raíz del repositorio, copia el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

Abre `.env` y configura las variables correspondientes:

```dotenv
SUPPLYCHAIN_JWT_SECRET=REEMPLAZA_CON_UN_SECRETO_ALEATORIO
SUPPLYCHAIN_STORAGE_SECRET=REEMPLAZA_CON_OTRO_SECRETO_ALEATORIO
AZURE_OPENAI_ENDPOINT=https://TU-RECURSO.services.ai.azure.com/openai/v1
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

### Variables utilizadas

| Variable | Descripción |
|---|---|
| `SUPPLYCHAIN_JWT_SECRET` | Secreto utilizado para firmar los tokens JWT. Debe tener al menos 32 caracteres. |
| `SUPPLYCHAIN_STORAGE_SECRET` | Secreto independiente para el almacenamiento de sesiones de NiceGUI. Debe tener al menos 32 caracteres y ser diferente del secreto JWT. |
| `AZURE_OPENAI_ENDPOINT` | Endpoint del recurso de Azure, incluida la ruta `/openai/v1`. |
| `AZURE_OPENAI_DEPLOYMENT` | Nombre del despliegue de modelo disponible en el recurso. |

Para generar un secreto aleatorio desde Python puedes ejecutar:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Genera dos valores diferentes con el comando anterior: uno para `SUPPLYCHAIN_JWT_SECRET` y otro para `SUPPLYCHAIN_STORAGE_SECRET`. Copia cada valor en su variable correspondiente dentro de `.env`. No publiques ni compartas estos secretos.

El endpoint y el despliegue se leen desde variables de entorno; no deben configurarse mediante valores reales incrustados en el código.

Si Azure OpenAI no está configurado o disponible, `AIDemandAgent` utiliza el promedio histórico como respaldo (`fallback_used: true`). El resto del análisis puede continuar funcionando.

### 7.1 Autenticación con Azure

El cliente centralizado se encuentra en:

```text
app/core/azure_openai.py
```

La aplicación utiliza `DefaultAzureCredential` de Azure Identity para obtener un token de Microsoft Entra ID.

Si utilizas Azure CLI, inicia sesión:

```powershell
az login
```

Comprueba la suscripción activa:

```powershell
az account show
```

La identidad seleccionada debe contar con los permisos necesarios para invocar el despliegue de Azure OpenAI.

La autenticación correcta no garantiza por sí sola que el servicio esté disponible. También deben coincidir el endpoint, el despliegue y los permisos.

## 8. Iniciar la aplicación

La solución utiliza dos procesos independientes:

- FastAPI: puerto `8000`.
- NiceGUI: puerto `8080`.

### 8.1 Iniciar FastAPI

En una primera terminal:

```powershell
python -m uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en:

http://127.0.0.1:8000/docs

Mantén esta terminal abierta.

### 8.2 Iniciar NiceGUI

En una segunda terminal, desde la raíz del proyecto:

```powershell
python -m app.ui
```

La interfaz web estará disponible en:

http://127.0.0.1:8080

Mantén también esta terminal abierta.

Para detener los procesos, presiona `Ctrl + C` en cada terminal.

## 9. Registro e inicio de sesión

El sistema dispone de los siguientes endpoints:

- `POST /api/auth/register`: registro de usuarios.
- `POST /api/auth/login`: autenticación y emisión del token.

### Opción 1. Crear el usuario de demostración (recomendado)

Para facilitar la evaluación del sistema, se incluye un script que crea una cuenta de demostración directamente en SQLite.

Desde la carpeta raíz del proyecto, ejecutar:

```powershell
python -m scripts.crear_usuario_demo
```

El script inicializa la base de datos si es necesario y registra al usuario utilizando el mismo mecanismo de hash de contraseñas que utiliza la API. Utiliza `INSERT OR IGNORE`, por lo que puede ejecutarse varias veces sin duplicar la cuenta.

**Credenciales de demostración:**

- Correo: `demo@supplychain.example.com`
- Contraseña: `DemoSupplyChain2026`

Después de crear la cuenta:

1. Iniciar FastAPI.
2. Iniciar NiceGUI.
3. Abrir http://127.0.0.1:8080.
4. Iniciar sesión con las credenciales de demostración.

### Opción 2. Registrar un usuario desde la API

También es posible registrar una cuenta manualmente:

1. Iniciar FastAPI.
2. Abrir http://127.0.0.1:8000/docs.
3. Localizar `POST /api/auth/register`.
4. Seleccionar **Try it out**.
5. Enviar un correo válido y una contraseña de entre 12 y 128 caracteres.

Ejemplo ficticio:

```json
{
  "email": "usuario@ejemplo.com",
  "password": "EjemploSeguro123!"
}
```

6. Ejecutar la solicitud.
7. Abrir http://127.0.0.1:8080.
8. Iniciar sesión con la cuenta registrada.

La interfaz NiceGUI utiliza `POST /api/auth/login` para autenticar al usuario. La validación de credenciales se centraliza en la API.

## 10. Utilizar el sistema

Una vez autenticado, el usuario puede acceder al panel de análisis.

El formulario permite proporcionar información como:

- Identificador del producto.
- Demanda histórica.
- Periodos de pronóstico.
- Inventario actual.
- Identificador del proveedor.
- Indicadores de entregas a tiempo y calidad.
- Capacidad del proveedor.
- Tiempo de entrega en días.
- Días de retraso.
- Inventario de seguridad.

Los tres últimos parámetros se envían a la API y se propagan por LangGraph para su utilización en los agentes de inventario, abastecimiento y logística.

Los resultados pueden incluir:

- Pronóstico tradicional y pronóstico asistido por IA.
- Comparación de pronósticos.
- Evaluación de inventario.
- Evaluación de proveedores.
- Recomendaciones de abastecimiento y compras.
- Resultados logísticos.
- Alertas y resumen ejecutivo.

Las recomendaciones de compra son informativas: el sistema no ejecuta órdenes de compra reales ni se conecta automáticamente con sistemas externos de proveedores o transportistas.

### 10.1 Historial de análisis

Los análisis se almacenan en SQLite y quedan asociados al usuario autenticado.

La API ofrece:

- `GET /api/supply-chain/history`: consulta paginada del historial del usuario.
- `GET /api/supply-chain/history/{analysis_id}`: consulta del detalle de un análisis propio.

La API restringe las consultas al usuario autenticado. Un usuario no debe poder recuperar los análisis pertenecientes a otra cuenta.

La interfaz permite consultar el historial y acceder al detalle de los análisis disponibles para la sesión.

## 11. Ejecutar las pruebas automatizadas

Utiliza el intérprete del entorno virtual para evitar ejecutar pytest desde otra instalación de Python.

Con el entorno virtual activo:

```powershell
python -m pytest -v
```



**Última validación registrada:** 58 pruebas aprobadas (`58 passed in 47.90s`), ejecutadas el 10 de noviembre de 2026.

## 12. Solución de problemas

### Python no encuentra pytest

Comprueba el intérprete:

```powershell
python -c "import sys; print(sys.executable)"
```

Debe corresponder al entorno virtual `.venv`.

### NiceGUI no puede conectarse con FastAPI

Comprueba que FastAPI esté activo en el puerto `8000` y NiceGUI en el `8080`.

Abre:

http://127.0.0.1:8000/docs

### No se puede iniciar sesión

Comprueba que la cuenta esté registrada, que la API esté activa y que el correo y la contraseña sean correctos.

### Error de autenticación con Azure

Comprueba que exista una credencial disponible para `DefaultAzureCredential`, que la identidad tenga los permisos necesarios y que las variables de entorno sean correctas.

### Error al invocar Azure OpenAI

Comprueba conectividad, permisos, endpoint, nombre del despliegue y cuota disponible. Evita repetir llamadas innecesariamente.

### Puerto ocupado

Para revisar el puerto 8000:

```powershell
netstat -ano | findstr :8000
```

Para revisar el puerto 8080:

```powershell
netstat -ano | findstr :8080
```

Identifica el PID antes de detener cualquier proceso.

## 13. Seguridad

- No publiques secretos, contraseñas ni tokens en GitHub.
- Mantén `.env` fuera del repositorio mediante `.gitignore`.
- Utiliza `.env.example` únicamente con valores ficticios.
- No incluyas credenciales reales en la documentación.
- Protege los endpoints privados mediante autenticación.
- Mantén el aislamiento del historial por usuario.
- No publiques datos confidenciales de proveedores o inventarios.
- Si una credencial real se expone, revócala o rótala; eliminarla del archivo no la elimina del historial de Git.

## 14. Estructura principal del proyecto

```text
SupplyChainAgentic/
├── app/
│   ├── agents/
│   │   ├── ai_demand_agent.py
│   │   ├── demand_agent.py
│   │   ├── inventory_agent.py
│   │   ├── logistics_agent.py
│   │   ├── purchasing_agent.py
│   │   ├── sourcing_agent.py
│   │   └── supplier_monitoring_agent.py
│   ├── auth/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── routes.py
│   │   └── security.py
│   ├── core/
│   │   └── azure_openai.py
│   ├── orchestration/
│   │   └── supply_chain_graph.py
│   ├── main.py
│   ├── supply_chain_database.py
│   └── ui.py
├── docs/
│   └── MVP.md
├── frontend/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── SupplyChainAgentic.pyproj
```

`app/agents/` contiene los agentes especializados; `app/auth/` concentra la autenticación; `app/orchestration/` define el flujo de LangGraph; y `app/supply_chain_database.py` administra la persistencia de los análisis.

La interfaz actualmente implementada para el MVP es NiceGUI. La carpeta `frontend/` conserva una plantilla de Vite y no constituye una interfaz React integrada al flujo funcional del MVP.

## 15. Uso de asistencia de inteligencia artificial

Durante el desarrollo y la documentación de SupplyChainAgentic se utilizó un asistente de inteligencia artificial como apoyo para tareas de escritura, revisión y mejora del código.

Las propuestas generadas se revisan y validan por el desarrollador mediante inspección del código, pruebas automatizadas y comprobaciones de funcionamiento. La responsabilidad sobre la integración y validación final del proyecto corresponde al desarrollador.

## 16. Estado del proyecto

SupplyChainAgentic cuenta con una API FastAPI, una interfaz NiceGUI, autenticación JWT, persistencia SQLite, orquestación LangGraph y agentes especializados para apoyar el análisis de la cadena de suministro.

El pronóstico asistido por IA está integrado mediante Azure OpenAI. Los demás agentes trabajan principalmente con reglas y cálculos deterministas.

El sistema constituye una base funcional para demostrar la coordinación de agentes y la generación de recomendaciones. Las integraciones empresariales y el despliegue productivo quedan sujetos a futuras etapas de desarrollo y validación
