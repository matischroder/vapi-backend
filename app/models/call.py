from datetime import datetime, date
from fastapi import HTTPException

from app.services.vapi_service import VapiService
from app.services.dynamo_db.payment_promises import DynamoDBPromiseService

payment_promise_dynamo_service = DynamoDBPromiseService()


class Call:
    def __init__(
        self,
        debt_id,
        user_phone_number,
        project_id,
        campaign_id,
        assistant_id,
        company_phone_id,
        debt_amount,
        prompt,
        first_message,
        company_name=None,
        user_name=None,
    ):
        self.debt_id = debt_id
        self.user_phone_number = user_phone_number
        self.project_id = project_id
        self.campaign_id = campaign_id
        self.assistant_id = assistant_id
        self.company_phone_id = company_phone_id
        self.debt_amount = debt_amount
        self.prompt = prompt
        self.first_message = first_message
        self.company_name = company_name
        self.user_name = user_name
        self.vapi_service = VapiService()

    async def create_call(self):

        first_message_updated = self.first_message.replace(
            "MONTO_DEUDA", str(self.debt_amount)
        )
        payload = {
            "userPhoneNumber": self.user_phone_number,
            "phoneNumberId": self.company_phone_id,
            "assistantId": self.assistant_id,
            "firstMessage": first_message_updated,
        }
        await self.vapi_service.create_call(payload=payload)

    def create_promise(self, data):
        try:
            print(data)
            self.call_id = data.get("call", {}).get("id", {})
            if not data.get("functionCall"):
                return "Por favor, ¿me puede decir cuál es la operación que desea realizar?"
            # Agregar "T00:00:00" para completar el formato en caso de ser necesario
            if data.get("functionCall").get("name") == "crear_promesa_pago":
                fun = data.get("functionCall")
                if not fun.get("parameters"):
                    return "No pude entender bien su solicitud. Por favor, ¿me puede decir cuál es la fecha y el monto que quiere abonar de su deuda?"
                parameters = fun.get("parameters")
                amount = parameters.get("amount", {})
                datetime_str = parameters.get("datetime", {})
                if len(datetime_str) == 10:
                    datetime_str += "T00:00:00"
                if datetime_str.endswith("Z"):
                    datetime_str = datetime_str.rstrip("Z")
                if datetime_str.endswith(".000"):
                    datetime_str = datetime_str.rstrip(".000")
                datetime_obj = datetime.strptime(
                    datetime_str, "%Y-%m-%dT%H:%M:%S"
                ).date()
                print(f"amount {amount} time {datetime_str}")
                print(
                    f"{datetime_obj} {date.today()} {type(datetime_obj)} {type(date.today())}"
                )
                if datetime_obj < date.today():
                    return "Disculpe, pero no pude procesar bien en el sistema la fecha a la que se refiere. Por favor, ¿puede indicar la fecha específica con día, mes y año en la que quiere realizar el pago para evitar confusiones?"
                if datetime_obj == date.today():
                    return "Le hemos enviado un email así puede realizar el pago ahora mismo."
                if not amount:
                    return "No me quedo claro cuál es el monto que quiere pagar de la dueda ¿Me puede decir cuál es el monto de la deuda que quiere abonar?"
                if not datetime_obj:
                    return "No me quedo claro la fecha en la que quiere realizar el pago ¿Me puede decir la fecha exacta con dia, mes y año en la que quiere realizar el pago?"
                print(
                    f"Assistant id {self.assistant_id} customer phone number {self.user_phone_number}"
                )
                if not self.user_phone_number:
                    return "Veo que estas haciendo una prueba a traves del dashboard."

                print(float(amount), float(self.debt_amount))
                if float(amount) > float(self.debt_amount):
                    print("entro aca error de amount")
                    return f"Usted tiene una deuda de {self.debt_amount}, no puede excederse de ese monto."

                create_item = payment_promise_dynamo_service.create_payment_promise(
                    self.project_id,
                    self.campaign_id,
                    self.assistant_id,
                    self.call_id,
                    self.user_phone_number,
                    float(amount),
                    datetime_obj,
                )
                if create_item:
                    return f"Perfecto, hemos registrado que el día {datetime_str} va a realizar el pago de {amount} pesos. Nos estaremos comunicando ese día para recordarle que realice el pago."
            return "No hemos podido procesar de forma correcta su solicitud ¿Puede repetir?"

        except ValueError as ve:
            print(f"ValueError: {ve}")
            raise HTTPException(
                status_code=422,
                detail=f"Hubo un error con la fecha proporcionada: {ve}",
            )
        except KeyError as ke:
            print(f"KeyError: {ke}")
            raise HTTPException(
                status_code=422, detail=f"Faltan datos necesarios: {ke}"
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=500, detail=f"Hubo un error inesperado: {e}"
            )
