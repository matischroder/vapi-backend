from app.services.vapi_service import VAPIService


class Call:
    def __init__(
        self,
        user_id,
        project_id,
        campaign_id,
        assistant_id,
        amount,
        company_name,
        debt_amount,
        user_name=None,
    ):
        self.user_id = user_id
        self.project_id = project_id
        self.campaign_id = campaign_id
        self.assistant_id = assistant_id
        self.amount = amount
        self.company_name = company_name
        self.debt_amount = debt_amount
        self.user_name = user_name

    def create_call(self):
        prompt = f"{self.company_name} {self.debt_amount}"
        # call_request = CallRequest(firstMessage=prompt, context=self.user_name)
        vapi_service = VAPIService()
        vapi_service.create_call(
            self.user_id,
            self.project_id,
            self.campaign_id,
            self.assistant_id,
            call_request.dict(),
        )

    def create_promise(self):
        # Método para crear una promesa de pago
        # Implementa la lógica necesaria aquí
        pass
