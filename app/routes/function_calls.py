import json
from datetime import date, datetime
from fastapi import APIRouter, HTTPException

from app.models.function_calls import FunctionCallRequest, UserData
from app.utils.get_user_info import get_user_info
from app.services.vapi_service import VapiService
from app.services.dynamo_db.payment_promises import DynamoDBPromiseService

router = APIRouter()
payment_promise_dynamo_service = DynamoDBPromiseService()

# active_calls = set()


@router.post("")
async def function_call(request: FunctionCallRequest):
    try:
        data = request.message
        print("data", data)
        call_id = data.get("call", {}).get("id", {})
        # if call_id in active_calls:
        #     return "Por favor, espere unos minutos más en línea"
        # else:
        #     active_calls.add(call_id)
        if not data.get("functionCall"):
            # active_calls.discard(call_id)
            return "Por favor, ¿me puede decir cuál es la operación que desea realizar?"
        if len(datetime_str) == 10:
            # Agregar "T00:00:00" para completar el formato
            datetime_str += "T00:00:00"
        if data.get("functionCall").get("name") == "crear_promesa_pago":
            fun = data.get("functionCall")
            if not fun.get("parameters"):
                # active_calls.discard(call_id)
                return "Por favor, ¿me puede decir cuál es la fecha y el monto que quiere abonar de su deuda?"
            parameters = fun.get("parameters")
            amount = parameters.get("amount", {})
            datetime_str = parameters.get("datetime", {})
            if datetime_str.endswith("Z"):
                datetime_str = datetime_str.rstrip("Z")
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S").date()
            print(f"amount {amount} time {datetime_str}")
            print(
                f"{datetime_obj} {date.today()} {type(datetime_obj)} {type(date.today())}"
            )
            if datetime_obj < date.today():
                # active_calls.discard(call_id)
                print("ME VOY ACA")
                return "Disculpe, pero no hemos entendido bien la fecha a la que se refiere. Por favor, ¿puede indicar la fecha específica en la que quiere realizar el pago?"
            if datetime_obj == date.today():
                # active_calls.discard(call_id)
                return (
                    "Le hemos enviado un email así puede realizar el pago ahora mismo."
                )
            if not amount:
                # active_calls.discard(call_id)
                return "¿Me puede decir cuál es el monto de la deuda que quiere abonar?"
            if not datetime_obj:
                # active_calls.discard(call_id)
                return "¿Me puede decir cuándo quiere realizar el pago?"
            assistant_id = data.get("call", {}).get("assistantId")
            customer_number = data.get("customer", {}).get("number")
            print(
                f"Assistant id {assistant_id} customer phone number {customer_number}"
            )
            # if not customer_number:
            #     # active_calls.discard(call_id)
            #     return "Veo que estas haciendo una prueba a traves del dashboard."
            # user_debt_data: UserData = await get_user_info(
            #     assistant_id, customer_number
            # )
            # print(float(amount), float(user_debt_data.total_debt_amount))
            # if float(amount) > float(user_debt_data.total_debt_amount):
            #     print("entro aca error de amount")
            #     # active_calls.discard(call_id)
            #     return f"Usted tiene una deuda de {user_debt_data}, no puede excederse de ese monto."

            # create_item = payment_promise_dynamo_service.create_payment_promise(
            #     user_debt_data.project_id,
            #     user_debt_data.campaign_id,
            #     assistant_id,
            #     call_id,
            #     user_debt_data.user_phone_number,
            #     float(amount),
            #     datetime_obj,
            # )
            # if create_item:
            #     # active_calls.discard(call_id)
            return f"Perfecto, hemos registrado que el día {datetime_str} va a realizar el pago de {amount} pesos. Nos estaremos comunicando ese día para recordarle que realice el pago."
        # active_calls.discard(call_id)
        return "¿Puede repetir?"
    except Exception as e:
        # return "Hubo un error, por favor, ¿puede repetirme cuando desea pagar la deuda?"
        print(e)
        # active_calls.discard(call_id)
        raise HTTPException(status_code=422, detail=str(e))
