class PurchasingAgent:
    """
    Agente especializado en generar recomendaciones de compra.
    """

    def recommend_purchase(
        self,
        product_id: str,
        quantity: float
    ) -> dict:

        if quantity <= 0:
            return {
                "agent": "PurchasingAgent",
                "purchase_required": False,
                "message": "No se requiere realizar una compra."
            }

        return {
            "agent": "PurchasingAgent",
            "purchase_required": True,
            "product_id": product_id,
            "recommended_quantity": quantity,
            "action": "CREATE_PURCHASE_RECOMMENDATION"
        }
