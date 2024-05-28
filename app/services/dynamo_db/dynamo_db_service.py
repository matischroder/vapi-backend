import boto3
from boto3.dynamodb.conditions import Key


class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("Projects")

    def get_phone_numbers(self, project_id):
        response = self.table.get_item(Key={"project_id": project_id})
        return response["Item"]["vapi_phone_numbers"] if "Item" in response else []

    def update_phone_numbers(self, project_id, phone_numbers):
        self.table.update_item(
            Key={"project_id": project_id},
            UpdateExpression="SET vapi_phone_numbers = :val",
            ExpressionAttributeValues={":val": phone_numbers},
        )
