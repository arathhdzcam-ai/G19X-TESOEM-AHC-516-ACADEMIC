
import json
import math
from statistics import mean

from app.core.azure_openai import client, DEPLOYMENT_NAME


class AIDemandAgent:
    """
    Agente de demanda con Azure OpenAI y alternativa determinista
    para que los errores del servicio no interrumpan la orquestación.
    """

    @staticmethod
    def _fallback_analysis(historical_demand: list[float]) -> dict:
        """Genera un pronóstico local si la IA no está disponible."""

        average_demand = round(mean(historical_demand), 2)

        if len(historical_demand) < 2:
            trend = "estable"
        elif historical_demand[-1] > historical_demand[0]:
            trend = "creciente"
        elif historical_demand[-1] < historical_demand[0]:
            trend = "decreciente"
        else:
            trend = "estable"

        return {
            "trend": trend,
            "average_demand": average_demand,
            "forecast_demand": average_demand,
            "demand_variability": "media",
            "risk": "medio",
            "recommendation": (
                "Pronóstico calculado mediante el promedio histórico. "
                "Revisar la demanda y actualizar el análisis cuando "
                "el servicio de IA esté disponible."
            ),
        }

    @staticmethod
    def _valid_number(value) -> bool:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            and value >= 0
        )

    def analyze(self, historical_demand: list[float]) -> dict:
        if not historical_demand:
            raise ValueError(
                "La demanda histórica no puede estar vacía."
            )

        if any(
            not self._valid_number(value)
            for value in historical_demand
        ):
            raise ValueError(
                "La demanda histórica debe contener números "
                "finitos y no negativos."
            )

        prompt = f"""
Analiza la siguiente demanda histórica:

{historical_demand}

Genera un pronóstico para el siguiente periodo.

Devuelve únicamente un objeto JSON válido con esta estructura:

{{
    "trend": "creciente|estable|decreciente",
    "average_demand": numero,
    "forecast_demand": numero,
    "demand_variability": "baja|media|alta",
    "risk": "bajo|medio|alto",
    "recommendation": "recomendación breve"
}}

El promedio debe corresponder a la demanda histórica.
El pronóstico debe ser numérico, finito y no negativo.
No agregues explicaciones fuera del JSON.
"""

        try:
            response = client.responses.create(
                model=DEPLOYMENT_NAME,
                input=prompt,
            )

            analysis = json.loads(response.output_text)

            if not isinstance(analysis, dict):
                raise ValueError("La respuesta no es un objeto JSON.")

            average = analysis.get("average_demand")
            forecast = analysis.get("forecast_demand")

            if not self._valid_number(average):
                raise ValueError("El promedio de la IA no es válido.")

            if not self._valid_number(forecast):
                raise ValueError("El pronóstico de la IA no es válido.")

            analysis.setdefault("trend", "estable")
            analysis.setdefault("demand_variability", "media")
            analysis.setdefault("risk", "medio")
            analysis.setdefault(
                "recommendation",
                "Pronóstico generado mediante Azure OpenAI.",
            )

            return {
                "agent": "AIDemandAgent",
                "historical_demand": historical_demand,
                "method": "azure_openai",
                "fallback_used": False,
                "analysis": analysis,
            }

        except Exception:
            # No propagamos errores del servicio o de su respuesta.
            # El flujo de Supply Chain puede continuar con el promedio.
            return {
                "agent": "AIDemandAgent",
                "historical_demand": historical_demand,
                "method": "historical_average_fallback",
                "fallback_used": True,
                "analysis": self._fallback_analysis(
                    historical_demand
                ),
            }
