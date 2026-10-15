class SupplierMonitoringAgent:
    """
    Agente especializado en monitorear el riesgo de proveedores.
    """

    def analyze(
        self,
        supplier_id: str,
        on_time_delivery_rate: float,
        quality_rate: float,
        capacity: float
    ) -> dict:
        """
        Analiza el desempeño y riesgo de un proveedor.
        """

        risk_factors = 0

        if on_time_delivery_rate < 0.90:
            risk_factors += 1

        if quality_rate < 0.95:
            risk_factors += 1

        if capacity <= 0:
            risk_factors += 1

        if risk_factors == 0:
            risk = "low"

        elif risk_factors == 1:
            risk = "medium"

        else:
            risk = "high"

        return {
            "agent": "SupplierMonitoringAgent",
            "supplier_id": supplier_id,
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rate": quality_rate,
            "capacity": capacity,
            "risk": risk,
            "risk_factors": risk_factors
        }