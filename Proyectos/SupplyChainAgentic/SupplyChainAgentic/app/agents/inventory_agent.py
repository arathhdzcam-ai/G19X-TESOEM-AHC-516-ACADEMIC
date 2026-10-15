class InventoryAgent:
    """
    Agente especializado en analizar niveles de inventario.
    """

    def __init__(self, safety_stock: float = 20):
        self.safety_stock = safety_stock

    def analyze(
        self,
        current_inventory: float,
        forecast_demand: float
    ) -> dict:
        """
        Analiza si el inventario actual es suficiente
        para cubrir la demanda pronosticada.
        """

        required_inventory = forecast_demand + self.safety_stock

        inventory_status = (
            "sufficient"
            if current_inventory >= required_inventory
            else "low"
        )

        recommended_order = max(
            0,
            required_inventory - current_inventory
        )

        return {
            "agent": "InventoryAgent",
            "current_inventory": current_inventory,
            "forecast_demand": forecast_demand,
            "safety_stock": self.safety_stock,
            "required_inventory": required_inventory,
            "inventory_status": inventory_status,
            "recommended_order": recommended_order
        }