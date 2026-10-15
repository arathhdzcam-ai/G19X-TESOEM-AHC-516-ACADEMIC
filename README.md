\# SupplyChainAgentic



\## Descripción del proyecto



SupplyChainAgentic es un proyecto académico orientado al diseño e implementación de una arquitectura basada en agentes inteligentes especializados para la gestión de la cadena de suministro (\*Supply Chain\*).



La solución busca coordinar diferentes agentes para analizar la demanda, evaluar inventarios y apoyar la toma de decisiones relacionadas con el abastecimiento y las compras.



\## Objetivo general



Desarrollar una arquitectura Agentic para optimizar integralmente la cadena de suministro mediante agentes inteligentes y mecanismos de orquestación.



\## Funcionalidades principales



\- Análisis y pronóstico de la demanda.

\- Análisis de inventarios.

\- Evaluación de necesidades de abastecimiento.

\- Generación de recomendaciones para compras.

\- Coordinación de agentes mediante una capa de orquestación.

\- Exposición de funcionalidades mediante una API.

\- Integración con servicios de inteligencia artificial de Azure, cuando estén configurados.



\## Tecnologías



\- Python

\- FastAPI

\- LangGraph

\- Azure OpenAI

\- Git y GitHub



\## Requisitos



\- Python 3.12 o una versión compatible con las dependencias del proyecto.

\- Git.

\- Visual Studio con soporte para Python.

\- Credenciales y configuración de Azure OpenAI para las funciones que utilizan ese servicio.



\## Instalación y ejecución



\### 1. Clonar el repositorio



```powershell

git clone https://github.com/arathhdzcam-ai/G19X-TESOEM-AHC-516-ACADEMIC.git

cd G19X-TESOEM-AHC-516-ACADEMIC

```



\### 2. Crear y activar un entorno virtual



En Windows PowerShell:



```powershell

python -m venv .venv

.\\\\.venv\\\\Scripts\\\\Activate.ps1

```



\### 3. Instalar las dependencias



Instala las dependencias especificadas por el proyecto. Si el repositorio incluye un archivo `requirements.txt`, ejecuta:



```powershell

pip install -r requirements.txt

```



\### 4. Iniciar la API



Desde la carpeta del proyecto, ejecuta:



```powershell

python -m uvicorn app.main:app --reload

```



La documentación interactiva de la API estará disponible en:



http://127.0.0.1:8000/docs



\## Seguridad



Las claves de Azure y otros datos sensibles deben configurarse mediante variables de entorno o mecanismos seguros de autenticación. No se deben publicar contraseñas, claves de API ni archivos con credenciales en GitHub.



\## Estado del proyecto



Proyecto académico en desarrollo. Las funcionalidades disponibles dependen de la configuración local y de los servicios externos conectados.



\## Autor



\- Nombre: \[Escribe tu nombre]

\- Institución: \[Escribe tu institución]

