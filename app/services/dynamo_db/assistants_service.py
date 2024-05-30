from decimal import Decimal
from boto3.dynamodb.conditions import Key

from .db_utils import dynamodb_resource


class DynamoDBAssistantsService:
    def __init__(self):
        self.dynamodb = dynamodb_resource
        self.table_name = "assistants"
        self.assistants_table = self.dynamodb.Table(self.table_name)

    def create_assistant(
        self,
        assistant_id,
        project_id,
        first_message,
        prompt,
        voice_provider,
        voice_id,
        voice_speed,
    ):
        try:
            elements = {
                "assistant_id": assistant_id,
                "project_id": project_id,
                "first_message": first_message,
                "prompt": prompt,
                "voice_provider": voice_provider,
                "voice_id": voice_id,
                "voice_speed": Decimal(str(voice_speed)),
            }
            self.assistants_table.put_item(Item=elements)
            return elements
        except Exception as e:
            print(f"Error creating assistant: {e}")
            return None

    def get_project_assistants(self, project_id):
        try:
            response = self.assistants_table.query(
                IndexName="project_id-index",
                KeyConditionExpression=Key("project_id").eq(project_id),
            )
            return response.get("Items", [])
        except Exception as e:
            print(f"Error fetching assistants for project: {e}")
            return None

    def get_assistant(self, assistant_id):
        try:
            response = self.assistants_table.get_item(
                Key={"assistant_id": assistant_id}
            )
            return response.get("Item", None)
        except Exception as e:
            print(f"Error fetching assistant: {e}")
            return None

    def update_assistant(self, assistant_id, update_data):
        update_expression = "SET " + ", ".join(
            [f"{k}=:{k}" for k in update_data.keys()]
        )
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}

        try:
            response = self.assistants_table.update_item(
                Key={"assistant_id": assistant_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
            return response
        except Exception as e:
            print(f"Error updating assistant: {e}")
            return None

    def delete_assistant(self, assistant_id):
        try:
            response = self.assistants_table.delete_item(
                Key={"assistant_id": assistant_id}
            )
            return response
        except Exception as e:
            print(f"Error deleting assistant: {e}")
            return None
