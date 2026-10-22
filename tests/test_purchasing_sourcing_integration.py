from app.orchestration.supply_chain_graph import analyze_purchasing


def test_purchasing_respects_supplier_capacity():
    state = {
        "product_id": "SKU-TEST",
        "sourcing_result": {
            "recommended_quantity": 30,
            "unmet_quantity": 40,
        },
    }

    result = analyze_purchasing(state)
    purchasing = result["purchasing_result"]

    assert purchasing["purchase_required"] is True
    assert purchasing["recommended_quantity"] == 30
    assert purchasing["unmet_quantity"] == 40
