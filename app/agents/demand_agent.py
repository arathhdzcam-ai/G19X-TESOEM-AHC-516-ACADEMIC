from statistics import mean


class DemandAgent:
    """
    Agente especializado en análisis y pronóstico de demanda.
    """

    def __init__(self, forecast_periods: int = 3):
        self.forecast_periods = forecast_periods

    def forecast(self, historical_demand: list[float]) -> dict:
        """
        Genera un pronóstico básico utilizando el promedio
        de la demanda histórica.
        """

        if not historical_demand:
            raise ValueError("La demanda histórica no puede estar vacía.")

        average_demand = mean(historical_demand)

        forecast = [
            round(average_demand, 2)
            for _ in range(self.forecast_periods)
        ]

        return {
            "agent": "DemandAgent",
            "method": "historical_average",
            "historical_demand": historical_demand,
            "average_demand": round(average_demand, 2),
            "forecast": forecast,
            "forecast_periods": self.forecast_periods
        }