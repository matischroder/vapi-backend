import requests
from app.config import Config


async def fetch_external_data(query_param: str) -> dict:
    url = f"{Config.EXTERNAL_API_URL}/endpoint"
    headers = {"Authorization": f"Bearer {Config.EXTERNAL_API_KEY}"}
    params = {"param": query_param}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from external API"}
