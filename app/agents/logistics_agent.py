
class LogisticsAgent:
    """Evalúa el desempeño logístico y la prioridad de entrega."""

    def analyze(
        self,
        on_time_delivery_rate: float,
        lead_time_days: float,
        delay_days: float = 0,
    ) -> dict:
        if not 0 <= on_time_delivery_rate <= 100:
            raise ValueError(
                "La tasa de entregas a tiempo debe estar entre 0 y 100."
            )

        if lead_time_days < 0 or delay_days < 0:
            raise ValueError(
                "Los tiempos de entrega y retraso no pueden ser negativos."
            )

        # Admite tasas expresadas como fracción (0.95) o porcentaje (95).
        rate = (
            on_time_delivery_rate * 100
            if on_time_delivery_rate <= 1
            else on_time_delivery_rate
        )

        if delay_days > 0:
            delivery_status = "delayed"
        elif rate >= 95:
            delivery_status = "on_time_performance_good"
        else:
            delivery_status = "delivery_risk"

        if delay_days >= 3 or rate < 80:
            priority = "high"
        elif delay_days > 0 or rate < 95:
            priority = "medium"
        else:
            priority = "low"

        if delivery_status == "delayed":
            recommendation = "Revisar el retraso y actualizar la fecha estimada."
        elif delivery_status == "delivery_risk":
            recommendation = "Monitorear al proveedor y confirmar la entrega."
        else:
            recommendation = "Mantener el seguimiento habitual de la entrega."

        return {
            "agent": "LogisticsAgent",
            "on_time_delivery_rate": rate,
            "lead_time_days": lead_time_days,
            "delay_days": delay_days,
            "delivery_status": delivery_status,
            "priority": priority,
            "recommendation": recommendation,
        }
