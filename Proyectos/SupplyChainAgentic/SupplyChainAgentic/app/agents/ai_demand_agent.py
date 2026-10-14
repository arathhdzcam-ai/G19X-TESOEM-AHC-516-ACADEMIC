import json

from app.core.azure_openai import client, DEPLOYMENT_NAME


class AIDemandAgent:
    """
    Agente de demanda que utiliza Azure OpenAI
    para analizar y pronosticar la demanda.
    """

    def analyze(self, historical_demand: list[float]) -> dict:

        if not historical_demand:
            raise ValueError(
                "La demanda histórica no puede estar vacía."
            )

        prompt = f"""
Analiza la siguiente demanda histórica:

{historical_demand}

Genera un pronóstico de demanda para el siguiente periodo.

Devuelve UNICAMENTE un objeto JSON valido con esta estructura:

{{
    "trend": "creciente|estable|decreciente",
    "average_demand": numero,
    "forecast_demand": numero,
    "demand_variability": "baja|media|alta",
    "risk": "bajo|medio|alto",
    "recommendation": "recomendacion breve"
}}

Reglas:

1. average_demand debe ser el promedio de la demanda histórica.
2. forecast_demand debe ser una estimación numérica razonable para el siguiente periodo.
3. No agregues explicaciones fuera del JSON.
"""

        response = client.responses.create(
            model=DEPLOYMENT_NAME,
            input=prompt
        )

        analysis_text = response.output_text

        try:
            analysis = json.loads(analysis_text)

        except json.JSONDecodeError:

            analysis = {
                "trend": "unknown",
                "average_demand": None,
                "forecast_demand": None,
                "demand_variability": "unknown",
                "risk": "unknown",
                "recommendation": analysis_text
            }

        return {
            "agent": "AIDemandAgent",
            "historical_demand": historical_demand,
            "analysis": analysis
        }