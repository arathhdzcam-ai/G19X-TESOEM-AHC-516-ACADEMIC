from app.core.azure_openai import client, DEPLOYMENT_NAME


response = client.responses.create(
    model=DEPLOYMENT_NAME,
    input="Responde únicamente: Conexión desde la aplicación correcta."
)

print('hola...')
print(response.output_text)