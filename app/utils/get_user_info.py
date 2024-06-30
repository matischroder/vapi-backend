from app.models.function_calls import UserData
from app.services.dynamo_db.assistants_service import DynamoDBAssistantsService
from app.services.dynamo_db.campaigns_service import DynamoDBCampaignService
from app.services.dynamo_db.debts_service import DynamoDBDebtService

assistant_dynamo_service = DynamoDBAssistantsService()
campaign_dynamo_service = DynamoDBCampaignService()
debt_dynamo_service = DynamoDBDebtService()


def filter_user_debts(array: list, customer_number: str):
    return [
        item
        for item in array
        if item.get("status") == "PENDIENTE"
        and any(customer_number in phone for phone in item.get("phone", []))
    ]


def remove_plus_sign(phone_number):
    return phone_number.replace("+", "")


async def get_user_info(assistant_id: str, customer_number: str):
    formatted_customer_number = remove_plus_sign(customer_number)
    assistant_info = assistant_dynamo_service.get_assistant(assistant_id)
    project_id = assistant_info.get("project_id")
    all_project_debts = debt_dynamo_service.get_debts_by_project_id(project_id)
    print(assistant_info)
    if all_project_debts is not None:
        user_debts = filter_user_debts(all_project_debts, formatted_customer_number)
        print(user_debts)
        total_amount = sum(item.get("amount", 0) for item in user_debts)
        user_data = UserData(
            project_id=project_id,
            campaign_id=user_debts[0].get("campaign_id"),
            user_phone_number=formatted_customer_number,
            total_debt_amount=total_amount,
        )
        return user_data
    return "No hemos encontrado deudas a su nombre"
