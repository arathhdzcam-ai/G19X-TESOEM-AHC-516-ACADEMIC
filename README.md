# SupplyChainAgentic

**Arquitectura Agentic para la gestión inteligente de Supply Chain**

## 1. Descripción del proyecto

SupplyChainAgentic es una aplicación que implementa una arquitectura basada en agentes inteligentes especializados para apoyar el análisis y la toma de decisiones en la cadena de suministro.

La solución utiliza una capa de orquestación con LangGraph para coordinar los agentes y presenta los resultados mediante una interfaz web con autenticación de usuarios.

### Objetivo general

Desarrollar una arquitectura Agentic para optimizar integralmente la cadena de suministro mediante agentes inteligentes, integración de servicios de inteligencia artificial y automatización de procesos.

### Funcionalidades principales

- Análisis de demanda histórica y pronóstico de demanda mediante inteligencia artificial.
- Comparación de pronósticos.
- Análisis de inventario.
- Monitoreo de proveedores.
- Evaluación de necesidades de compra.
- Orquestación de agentes mediante LangGraph.
- API desarrollada con FastAPI.
- Interfaz web desarrollada con NiceGUI.
- Autenticación de usuarios.
- Integración con Azure OpenAI mediante Microsoft Entra ID.

## 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python 3.12 | Lenguaje principal |
| FastAPI | API y servicios del sistema |
| LangGraph | Orquestación de agentes |
| LangChain | Componentes para aplicaciones con modelos de lenguaje |
| Azure OpenAI | Análisis de demanda mediante IA |
| Microsoft Entra ID | Autenticación para acceder a Azure |
| NiceGUI | Interfaz web |
| SQLite | Persistencia local de los datos de autenticación |
| Pydantic | Validación de datos |
| Pytest | Pruebas automatizadas |
| Git y GitHub | Control de versiones |

## 3. Requisitos previos

Antes de instalar el proyecto, se necesita:

- Windows 10 u 11.
- Python 3.12.
- Git.
- Visual Studio con las herramientas de desarrollo de Python.
- Acceso al repositorio del proyecto.
- Una cuenta de Azure con permisos para utilizar el recurso de Azure OpenAI configurado.
- Una credencial compatible con `DefaultAzureCredential` de Azure Identity.

La aplicación se ejecuta localmente. Sin embargo, las operaciones que utilizan Azure OpenAI requieren acceso al servicio y pueden consumir cuota o generar cargos según la suscripción y sus condiciones.

## 4. Obtener el código fuente

Abre PowerShell o la terminal de Visual Studio y ejecuta:

```powershell
git clone https://github.com/arathhdzcam-ai/G19X-TESOEM-AHC-516-ACADEMIC.git
```

Entra en la carpeta del repositorio:

```powershell
cd G19X-TESOEM-AHC-516-ACADEMIC
```

Comprueba que estás en la carpeta raíz del proyecto. Debes poder localizar archivos como `README.md`, `requirements.txt` y la carpeta `app`.

Si se trabaja desde Visual Studio, abre el proyecto `SupplyChainAgentic.pyproj` si está disponible en la copia descargada y utiliza una terminal situada en la carpeta raíz del proyecto.

## 5. Crear el entorno virtual de Python

Desde la carpeta raíz del proyecto, ejecuta:

```powershell
py -3.12 -m venv .venv
```

Activa el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

La terminal debe mostrar `(.venv)` al principio de la línea.

Comprueba la versión de Python:

```powershell
python --version
```

Comprueba que se utiliza el intérprete del entorno virtual:

```powershell
python -c "import sys; print(sys.executable)"
```

La ruta debe terminar en:

```text
.venv\Scripts\python.exe
```

Si PowerShell impide activar el entorno por la política de ejecución, se puede utilizar temporalmente esta opción en la terminal actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después, vuelve a ejecutar el comando de activación. Esta opción solo modifica la política de ejecución de la sesión actual de PowerShell.

## 6. Instalar las dependencias

Con el entorno virtual activo, ejecuta:

```powershell
python -m pip install --upgrade pip
```

Instala las dependencias declaradas en `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Comprueba que no existan conflictos conocidos entre las dependencias:

```powershell
python -m pip check
```

El resultado esperado es:

```text
No broken requirements found.
```

## 7. Configurar el acceso a Azure OpenAI

El proyecto utiliza el cliente centralizado definido en:

```text
app/core/azure_openai.py
```

Actualmente, la configuración del proyecto utiliza el endpoint de Azure AI con la ruta `/openai/v1` y el despliegue `gpt-5-mini`.

Antes de ejecutar análisis que utilicen IA, comprueba que el endpoint y el nombre del despliegue correspondan al recurso al que tienes acceso.

### 7.1 Autenticarse con Azure

La aplicación utiliza `DefaultAzureCredential` para obtener las credenciales de Microsoft Entra ID.

Si Azure CLI está instalado y configurado, abre una terminal y ejecuta:

```powershell
az login
```

Comprueba la cuenta activa:

```powershell
az account show
```

Si existen varias suscripciones, selecciona la que contiene el recurso correspondiente antes de continuar.

La identidad utilizada debe tener los permisos necesarios para invocar el despliegue de Azure OpenAI. Si la autenticación falla, revisa la identidad seleccionada, los permisos asignados y la configuración del recurso.

No es necesario copiar claves, contraseñas ni tokens directamente en el código fuente.

**Importante:** autenticarse en Azure no garantiza por sí solo que el despliegue esté disponible. También deben ser correctos el endpoint, el nombre del modelo desplegado y los permisos de acceso.

## 8. Iniciar la aplicación

La aplicación tiene dos servicios que deben ejecutarse simultáneamente:

- API de FastAPI en el puerto `8000`.
- Interfaz web de NiceGUI en el puerto `8080`.

### 8.1 Iniciar la API

Abre la primera terminal de PowerShell en la carpeta raíz del proyecto y activa el entorno virtual si aún no está activo.

Ejecuta:

```powershell
python -m uvicorn app.main:app --reload
```

Espera a que aparezca un mensaje similar a:

```text
Application startup complete.
```

Mantén esta terminal abierta mientras utilizas la aplicación.

La documentación interactiva de la API está disponible en:

http://127.0.0.1:8000/docs

Esta página se utiliza para consultar y probar los endpoints. No sustituye a la interfaz web principal.

### 8.2 Iniciar la interfaz web

Abre una segunda terminal de PowerShell en la misma carpeta raíz.

Activa el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Inicia la interfaz:

```powershell
python -m app.ui
```

Mantén esta segunda terminal abierta.

Abre el navegador en:

http://127.0.0.1:8080

La pantalla de inicio de sesión de SupplyChainAgentic debe aparecer en esta dirección.

## 9. Crear una cuenta e iniciar sesión

La aplicación dispone de endpoints para registrar usuarios e iniciar sesión. Si todavía no existe una cuenta en la base de datos local, debe crearse antes de acceder al panel.

Para registrar la primera cuenta:

1. Confirma que la API de FastAPI esté ejecutándose.
2. Abre http://127.0.0.1:8000/docs.
3. Localiza `POST /api/auth/register`.
4. Selecciona **Try it out**.
5. Introduce un correo electrónico válido y una contraseña de entre 12 y 128 caracteres.

Ejemplo de estructura de la solicitud:

```json
{
  "email": "arath.hdz.cam@gmail.com",
  "password": "MiPrueba2026!ABC,"
}
```

El ejemplo es ilustrativo: utiliza una contraseña propia y no reutilices credenciales personales.

6. Ejecuta la solicitud y comprueba que el registro haya sido satisfactorio.
7. Regresa a http://127.0.0.1:8080.
8. Introduce el correo y la contraseña que acabas de registrar.

Una vez autenticado, utiliza el panel web para realizar los análisis de la cadena de suministro.

La cuenta se almacena en la base de datos local de autenticación del proyecto. Si se utiliza una instalación nueva, no se debe asumir que las cuentas existentes en otra computadora estarán disponibles.

## 10. Utilizar el sistema

Desde el panel de SupplyChainAgentic:

1. Introduce los datos de entrada solicitados por el formulario.
2. Ejecuta el análisis.
3. Espera a que finalice el procesamiento.
4. Consulta los resultados de los agentes.

El flujo de análisis puede incluir:

- Demanda histórica.
- Pronóstico de demanda mediante IA.
- Comparación de pronósticos.
- Análisis de inventario.
- Análisis de proveedores.
- Evaluación de compras.

El resultado depende de los datos introducidos, las reglas implementadas en los agentes y la disponibilidad del servicio de IA.

## 11. Ejecutar las pruebas automatizadas

Con el entorno virtual activo y desde la carpeta raíz, ejecuta:

```powershell
python -m pytest -q
```

Las pruebas automatizadas permiten verificar el comportamiento cubierto por los casos de prueba del proyecto.

En la versión comprobada durante el desarrollo se obtuvo el siguiente resultado:

```text
9 passed in 14.77s
```

El número y el resultado pueden variar si cambia el código, las dependencias o el conjunto de pruebas.

Las pruebas unitarias y automatizadas no sustituyen la comprobación manual del login, la interfaz, la API y el acceso a Azure OpenAI.

## 12. Solución de problemas frecuentes

### Python no encuentra pytest

Comprueba que el entorno virtual esté activo:

```powershell
python -c "import sys; print(sys.executable)"
```

La ruta debe corresponder al intérprete de `.venv`. Si falta alguna dependencia, vuelve a instalar las dependencias del proyecto.

### La interfaz no puede conectarse con FastAPI

Comprueba que el servidor de FastAPI esté activo en el puerto `8000` y que la interfaz esté ejecutándose en el puerto `8080`.

Abre la documentación de la API para comprobar que responde:

http://127.0.0.1:8000/docs

### No se puede iniciar sesión

Comprueba que hayas registrado una cuenta, que el correo y la contraseña sean correctos y que la base de datos local de autenticación esté disponible.

### Error de autenticación con Azure

Comprueba que la credencial de Microsoft Entra ID esté disponible para `DefaultAzureCredential`, que la cuenta tenga permisos suficientes y que el endpoint y el despliegue sean correctos.

### El análisis falla al invocar Azure OpenAI

Comprueba la conectividad, los permisos, el despliegue, la disponibilidad del servicio y los límites de cuota. Evita repetir llamadas innecesariamente, ya que pueden consumir cuota.

### El puerto ya está ocupado

Si otro proceso está utilizando el puerto `8000` o `8080`, detén el proceso que corresponda o configura un puerto alternativo de manera consistente con la aplicación.

## 13. Seguridad

- No publiques claves, contraseñas, tokens ni secretos en GitHub.
- No incluyas credenciales reales en el README.
- Utiliza credenciales propias y seguras para crear la cuenta de acceso.
- Concede únicamente los permisos de Azure que sean necesarios.
- No ejecutes pruebas que invoquen Azure repetidamente sin comprobar antes su propósito y consumo potencial.
- No publiques datos confidenciales de proveedores, productos o inventarios.

## 14. Estructura principal del proyecto

```text
SupplyChainAgentic/
├── app/
│   ├── agents/
│   │   ├── ai_demand_agent.py
│   │   ├── demand_agent.py
│   │   ├── inventory_agent.py
│   │   ├── purchasing_agent.py
│   │   └── supplier_monitoring_agent.py
│   ├── auth/
│   ├── core/
│   │   └── azure_openai.py
│   ├── orchestration/
│   │   └── supply_chain_graph.py
│   ├── static/
│   ├── templates/
│   ├── main.py
│   └── ui.py
├── tests/
├── requirements.txt
├── README.md
└── SupplyChainAgentic.pyproj
```

La estructura anterior muestra los componentes principales. La presencia de archivos adicionales puede variar según la versión del repositorio.

## 15. Estado del proyecto

SupplyChainAgentic integra agentes especializados, una capa de orquestación con LangGraph, una API con FastAPI, una interfaz web con NiceGUI y un cliente de Azure OpenAI.

El proyecto está orientado a demostrar cómo coordinar agentes inteligentes para apoyar procesos de demanda, inventario, proveedores y compras dentro de una arquitectura de Supply Chain.


