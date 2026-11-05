# Scripts auxiliares

Esta carpeta contiene scripts para comprobaciones manuales de SupplyChainAgentic.

- test_ai_demand.py: prueba manual del agente de demanda.
- test_azure.py: comprueba Azure OpenAI mediante Entra ID.
- test_azure_live.py: prueba una solicitud real a Azure OpenAI.
- test_connection.py: comprueba la conexión con Azure OpenAI desde la aplicación.

Estos scripts no forman parte de las pruebas automatizadas de pytest.

Para ejecutar uno desde la raíz del proyecto:

    python -m scripts.test_ai_demand

Las pruebas automatizadas se encuentran en tests/.
