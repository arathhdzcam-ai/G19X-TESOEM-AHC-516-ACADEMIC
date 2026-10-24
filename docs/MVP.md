# MVP - SupplyChainAgentic

## 1. Descripción

SupplyChainAgentic es un proyecto académico que implementa una arquitectura basada en agentes inteligentes especializados para apoyar el análisis y la toma de decisiones en la cadena de suministro. Los agentes se coordinan mediante LangGraph y se exponen a través de una API desarrollada con FastAPI.

## 2. Objetivo

Desarrollar y validar un producto mínimo viable que permita analizar información de demanda, inventario y proveedores, generar recomendaciones y conservar los resultados para su consulta posterior.

## 3. Alcance funcional

El MVP contempla:

- Recepción y validación de datos para analizar la cadena de suministro.
- Análisis de demanda y generación de pronósticos.
- Evaluación de inventario.
- Análisis de proveedores.
- Apoyo a decisiones de compra cuando corresponda.
- Orquestación del flujo de agentes mediante LangGraph.
- Exposición de funcionalidades mediante FastAPI.
- Interfaz de usuario mediante NiceGUI.
- Persistencia de análisis en SQLite.
- Consulta paginada del historial de análisis.
- Aislamiento del historial por usuario.
- Pruebas automatizadas y documentación técnica.

## 4. Arquitectura tecnológica

| Componente | Tecnología |
|---|---|
| Lenguaje principal | Python |
| API | FastAPI |
| Orquestación de agentes | LangGraph |
| Integración de modelos y herramientas | LangChain |
| Interfaz de usuario | NiceGUI |
| Persistencia del MVP | SQLite |
| Integración de IA en Azure | Azure OpenAI, cuando esté configurado |
| Pruebas | pytest |
| Control de versiones | Git |

Las tecnologías adicionales previstas para la evolución de la arquitectura, como PostgreSQL, Redis, Azure AI Search, Docker, Kubernetes, Power BI, GitHub Actions y Microsoft Entra ID, deberán documentarse como implementadas únicamente cuando su integración esté comprobada.

## 5. Flujo general

1. El usuario proporciona los datos del producto, la demanda histórica, el inventario y la información del proveedor.
2. La API valida la solicitud.
3. LangGraph coordina los agentes de análisis.
4. Los agentes generan resultados y recomendaciones.
5. La aplicación consolida la respuesta.
6. El análisis se guarda en SQLite asociado al usuario correspondiente.
7. El usuario puede consultar su historial y los detalles de sus análisis.

## 6. Persistencia e historial

Cada análisis persistido debe conservar su identificador, producto, proveedor cuando corresponda, fecha de creación y resultado.

El historial debe permitir paginación y restringir las consultas a los registros del usuario autenticado. La consulta de un análisis perteneciente a otro usuario debe responder como recurso no encontrado.

La migración de la base de datos existente debe conservar los registros previos. Los registros históricos que no tengan propietario asignado deben permanecer sin atribución automática a un usuario.

## 7. Criterios de aceptación

- La suite de pruebas automatizadas termina sin fallos.
- Los endpoints de análisis e historial responden conforme a sus contratos.
- Los resultados pueden persistirse y recuperarse.
- La paginación del historial funciona.
- Un usuario no puede consultar los análisis de otro usuario.
- La migración de la base de datos conserva los registros existentes.
- La documentación describe el alcance real y distingue las funcionalidades implementadas de las futuras.

## 8. Validación actual

En la última ejecución de la suite de pruebas automatizadas se obtuvo el siguiente resultado:

`55 passed in 32.44s`

La ejecución terminó sin fallos. Este resultado valida las pruebas automatizadas existentes en ese momento, incluyendo las pruebas de persistencia, paginación, aislamiento del historial por usuario y migración de registros históricos.

Si se modifica el código o las pruebas, deberá ejecutarse nuevamente la suite y actualizarse este apartado con el resultado más reciente.

## 9. Fuera del alcance confirmado del MVP

No se considera implementada una integración de producción con PostgreSQL, Redis, Kubernetes, Power BI u otros servicios externos únicamente por estar previstos en la arquitectura. Su estado deberá verificarse de manera independiente.

## 10. Evolución prevista

- Consolidar la documentación de arquitectura y operación.
- Evaluar persistencia en PostgreSQL.
- Incorporar observabilidad y métricas.
- Evaluar despliegue con contenedores.
- Ampliar la analítica y las integraciones empresariales.
- Mantener pruebas automatizadas para cada funcionalidad incorporada.

