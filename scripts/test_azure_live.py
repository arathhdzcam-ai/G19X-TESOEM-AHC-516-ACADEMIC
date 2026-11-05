from app.core.azure_openai import client, DEPLOYMENT_NAME

try:
    response = client.responses.create(
        model=DEPLOYMENT_NAME,
        input="Responde solamente: conexion correcta",
    )

    print("Azure OpenAI: conexion correcta")
    print("Respuesta:", response.output_text)

except Exception as error:
    print("Error de Azure:", type(error).__name__)
    print(str(error)[:1000])
