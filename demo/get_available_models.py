from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
import os

api_url = os.getenv("WATSONX_URL")
api_key = os.getenv("WATSONX_API_KEY")
api_project_id = os.getenv("WATSONX_PROJECT_ID")

if not api_url or not api_key or not api_project_id:
    raise ValueError("Error: WATSONX_URL and WATSONX_API_KEY, WATSONX_PROJECT_ID environment variables must be set.")

# 1. Setup WatsonX Client & Model
api_client = APIClient(Credentials(
    url=api_url,
    api_key=api_key
))



api_client.foundation_models.ChatModels.show()