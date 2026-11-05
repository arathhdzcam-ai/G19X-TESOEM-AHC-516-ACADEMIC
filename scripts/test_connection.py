from app.core.azure_openai import client, DEPLOYMENT_NAME

response = client.responses.create(
    model=DEPLOYMENT_NAME,
    input="Responde unicamente: Conexion desde la aplicacion correcta."
)

print(response.output_text)
