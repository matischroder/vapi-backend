from .db_utils import dynamodb_resource
from botocore.exceptions import ClientError
from fastapi import HTTPException


class DynamoDBPhoneService:
    def __init__(self):
        self.dynamodb = dynamodb_resource
        self.projects_table = self.dynamodb.Table("projects")

    def get_project_phone_numbers(self, project_id: str):
        response = self.projects_table.get_item(Key={"project_id": project_id})
        project = response.get("Item", {})
        return project.get("vapi_phone_numbers", [])

    def update_project_phone_numbers(self, project_id, phone_numbers):
        self.projects_table.update_item(
            Key={"project_id": project_id},
            UpdateExpression="SET vapi_phone_numbers = :val",
            ExpressionAttributeValues={":val": phone_numbers},
        )
