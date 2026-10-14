from openai import OpenAI
from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider
)


ENDPOINT = (
    "https://226020019isc-1679-resource.services.ai.azure.com"
    "/openai/v1"
)

DEPLOYMENT_NAME = "gpt-5-mini"


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)


client = OpenAI(
    base_url=ENDPOINT,
    api_key=token_provider
)