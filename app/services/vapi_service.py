import requests
import httpx
from app.config import Config


class VapiService:
    BASE_URL = "https://api.vapi.ai"  # Añadir esta línea

    def __init__(self):
        self.auth_token = Config.VAPI_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        self.agents = {}

    @staticmethod
    async def create_assistant(payload: dict):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.post(
                f"{VapiService.BASE_URL}/assistant",
                headers=headers,
                json={
                    "name": payload.get("name"),
                    "firstMessage": payload.get("first_message"),
                    "model": {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": payload.get("prompt")}
                        ],
                        "provider": "openai",
                        "maxTokens": 250,
                        "temperature": 0.7,
                        "emotionRecognitionEnabled": True,
                    },
                    "voice": {
                        "provider": payload.get("voice_provider"),
                        "voiceId": payload.get("voice_id"),
                        "speed": payload.get("voice_speed"),
                    },
                },
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def update_assistant(assistant_id: str, payload: dict):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.patch(
                f"{VapiService.BASE_URL}/assistant/{assistant_id}",
                headers=headers,
                json={
                    "firstMessage": payload.get("first_message"),
                    "model": {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": payload.get("prompt")}
                        ],
                        "provider": "openai",
                        "maxTokens": 250,
                        "temperature": 0.7,
                        "emotionRecognitionEnabled": True,
                    },
                    "voice": {
                        "provider": payload.get("voice_provider"),
                        "voiceId": payload.get("voice_id"),
                        "speed": payload.get("voice_speed"),
                    },
                },
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def delete_assistant(assistant_id: str):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.delete(
                f"{VapiService.BASE_URL}/assistant/{assistant_id}",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_assistant(assistant_id: str):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.get(
                f"{VapiService.BASE_URL}/assistant/{assistant_id}",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def buy_phone_number(area_code: str):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.post(
                f"{VapiService.BASE_URL}/phone-number/buy",
                headers=headers,
                json={"areaCode": area_code},
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def import_twilio(
        twilioPhoneNumber: str, twilioAccountSid: str, twilioAuthToken: str, name: str
    ):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.post(
                f"{VapiService.BASE_URL}/phone-number/import/twilio",
                headers=headers,
                json={
                    "twilioPhoneNumber": twilioPhoneNumber,
                    "twilioAccountSid": twilioAccountSid,
                    "twilioAuthToken": twilioAuthToken,
                    "name": name,
                },
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def import_vonage(vonagePhoneNumber: str, credentialId: str, name: str):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.post(
                f"{VapiService.BASE_URL}/phone-number/import/vonage",
                headers=headers,
                json={
                    "vonagePhoneNumber": vonagePhoneNumber,
                    "credentialId": credentialId,
                    "name": name,
                },
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def delete_phone_number(phone_number_id: str):
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {Config.VAPI_API_KEY}",
                "Content-Type": "application/json",
            }
            response = await client.delete(
                f"{VapiService.BASE_URL}/phone-number/{phone_number_id}",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
