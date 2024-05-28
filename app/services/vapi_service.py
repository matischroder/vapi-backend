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

    def create_agent(
        self,
        agent_id,
        first_message,
        model_provider="openai",
        model_name="gpt-3.5-turbo",
        voice="jennifer-playht",
    ):
        agent = {
            "firstMessage": first_message,
            "model": {
                "provider": model_provider,
                "model": model_name,
                "messages": [{"role": "system", "content": "You are an assistant."}],
            },
            "voice": voice,
        }
        self.agents[agent_id] = agent
        return {"status": "success", "agent_id": agent_id, "agent": agent}

    def get_agent(self, agent_id):
        agent = self.agents.get(agent_id)
        if agent:
            return {"status": "success", "agent": agent}
        else:
            return {"status": "failed", "message": "Agent not found"}

    def list_agents(self):
        return {"status": "success", "agents": self.agents}

    def create_call(self, phone_number_id, customer_number, agent_id):
        agent = self.agents.get(agent_id)
        if not agent:
            return {"status": "failed", "message": "Agent not found"}

        data = {
            "assistant": agent,
            "phoneNumberId": phone_number_id,
            "customer": {
                "number": customer_number,
            },
        }

        response = requests.post(
            "https://api.vapi.ai/call/phone", headers=self.headers, json=data
        )

        if response.status_code == 201:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "failed", "message": response.text}

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
