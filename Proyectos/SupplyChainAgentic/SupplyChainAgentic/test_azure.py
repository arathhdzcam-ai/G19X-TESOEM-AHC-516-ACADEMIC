from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


endpoint = "https://226020019isc-1679-resource.services.ai.azure.com/openai/v1"
deployment_name = "gpt-5-mini"


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)


client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)


response = client.responses.create(
    model=deployment_name,
    input="Responde únicamente: Azure OpenAI conectado desde Visual Studio."
)


print(response.output_text)