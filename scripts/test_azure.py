
import os

from openai import OpenAI
from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)


endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not endpoint or not deployment_name:
    raise RuntimeError(
        "Configura AZURE_OPENAI_ENDPOINT y "
        "AZURE_OPENAI_DEPLOYMENT antes de ejecutar esta prueba."
    )

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default",
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)

response = client.responses.create(
    model=deployment_name,
    input="Responde únicamente: Azure OpenAI conectado desde Visual Studio.",
)

print(response.output_text)
