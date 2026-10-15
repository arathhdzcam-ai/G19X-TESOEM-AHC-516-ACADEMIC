
class SourcingAgent:
    """Calcula las necesidades de abastecimiento del producto."""

    def analyze(
        self,
        product_id: str,
        forecast_demand: float,
        current_inventory: float,
        safety_stock: float,
        supplier_capacity: float,
    ) -> dict:
        if not product_id.strip():
            raise ValueError("El identificador del producto es obligatorio.")

        if forecast_demand < 0 or current_inventory < 0:
            raise ValueError("La demanda y el inventario no pueden ser negativos.")

        if safety_stock < 0 or supplier_capacity < 0:
            raise ValueError("El stock de seguridad y la capacidad no pueden ser negativos.")

        required_inventory = forecast_demand + safety_stock
        shortage = max(0.0, required_inventory - current_inventory)
        recommended_quantity = min(shortage, supplier_capacity)
        unmet_quantity = max(0.0, shortage - recommended_quantity)

        if shortage == 0:
            status = "sufficient"
        elif unmet_quantity > 0:
            status = "insufficient_supplier_capacity"
        else:
            status = "replenishment_required"

        return {
            "agent": "SourcingAgent",
            "product_id": product_id,
            "forecast_demand": forecast_demand,
            "current_inventory": current_inventory,
            "safety_stock": safety_stock,
            "required_inventory": required_inventory,
            "shortage": shortage,
            "supplier_capacity": supplier_capacity,
            "recommended_quantity": recommended_quantity,
            "unmet_quantity": unmet_quantity,
            "status": status,
        }
