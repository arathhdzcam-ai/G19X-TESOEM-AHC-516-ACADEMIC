# Frontend - SupplyChainAgentic

Esta carpeta contiene el scaffold inicial de React y Vite.

## Estado actual

El frontend de React todavía no está integrado con el backend ni forma parte del flujo principal de ejecución.

La interfaz actualmente funcional de SupplyChainAgentic está desarrollada con NiceGUI y se comunica con la API de FastAPI.

## Ejecución actual del proyecto

Desde la raíz del repositorio:

- Backend: `python -m uvicorn app.main:app --reload`
- Interfaz: `python -m app.ui`

La interfaz estará disponible en `http://127.0.0.1:8080` y la documentación de la API en `http://127.0.0.1:8000/docs`.

## Trabajo futuro

Este scaffold puede utilizarse posteriormente para desarrollar una interfaz React integrada con los endpoints de FastAPI.
