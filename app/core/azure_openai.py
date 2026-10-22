
import os

from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)

# Cargar la configuración antes de crear el cliente.
load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

if not ENDPOINT:
    raise RuntimeError(
        "Falta AZURE_OPENAI_ENDPOINT en el archivo .env"
    )

if not DEPLOYMENT_NAME:
    raise RuntimeError(
        "Falta AZURE_OPENAI_DEPLOYMENT en el archivo .env"
    )

# Asegurar que la URL tenga la ruta de la API OpenAI v1.
if not ENDPOINT.endswith("/openai/v1"):
    if ENDPOINT.endswith("/openai"):
        ENDPOINT = f"{ENDPOINT}/v1"
    else:
        ENDPOINT = f"{ENDPOINT}/openai/v1"

# Autenticación mediante las credenciales de Azure.
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default",
)

# Crear el cliente una sola vez con la configuración correcta.
client = OpenAI(
    base_url=ENDPOINT,
    api_key=token_provider,
)
