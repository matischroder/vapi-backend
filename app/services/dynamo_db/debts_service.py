from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from .db_utils import dynamodb_client


class DynamoDBDebtService:

    def __init__(self):
        self.table_name = "debts"
        self.debtors_table_name = "debtors"
        self.users_table_name = "users"
        self.deserializer = TypeDeserializer()

    def deserialize_item(self, item):
        return {k: self.deserializer.deserialize(v) for k, v in item.items()}

    def get_debts_by_project_id(self, project_id: str):
        try:
            response = dynamodb_client.query(
                TableName=self.table_name,
                IndexName="project_id-index",
                KeyConditionExpression="project_id = :project_id",
                ExpressionAttributeValues={":project_id": {"S": project_id}},
            )

            items = response.get("Items", [])
            debts = [
                self.deserialize_item(item)
                for item in items
                if item.get("project_id", {}).get("S") == project_id
            ]
            if debts:
                print(f"Found {len(debts)} debts for project_id: {project_id}")
                return debts
            else:
                print(f"No debts found for project_id: {project_id}")
                return []

        except ClientError as e:
            print("An error occurred:", e)
            return None

    def get_debts_by_campaign_id(self, campaign_id: str):
        try:
            response = dynamodb_client.query(
                TableName=self.table_name,
                IndexName="campaign_id-index",
                KeyConditionExpression="campaign_id = :campaign_id",
                ExpressionAttributeValues={":campaign_id": {"S": campaign_id}},
            )

            items = response.get("Items", [])
            debts = [
                self.deserialize_item(item)
                for item in items
                if item.get("campaign_id", {}).get("S") == campaign_id
            ]
            if debts:
                print(f"Found {len(debts)} debts for campaign_id: {campaign_id}")
                return debts
            else:
                print(f"No debts found for campaign_id: {campaign_id}")
                return []

        except ClientError as e:
            print("An error occurred:", e)
            return None

    def get_debts_by_user_id(self, user_id: str):
        try:
            print(f"Scanning the Debts table for user_id: {user_id}")
            response = dynamodb_client.scan(
                TableName=self.table_name,
                FilterExpression="user_id = :user_id",
                ExpressionAttributeValues={":user_id": {"S": user_id}},
            )

            items = response["Items"]
            debts = [
                item for item in items if item.get("user_id", {}).get("S") == user_id
            ]

            if debts:
                print(f"Found {len(debts)} debts for user_id: {user_id}")
                return debts
            else:
                print(f"No debts found for user_id: {user_id}")
                return []

        except ClientError as e:
            print("An error occurred:", e)
            return None

    def get_debt_by_id(self, debt_id: str):
        try:
            print(f"Scanning the Debts table for debt_id: {debt_id}")
            response = dynamodb_client.get_item(
                TableName=self.table_name, Key={"id": {"S": debt_id}}
            )

            if "Item" in response:
                print(f"Found debt for debt_id: {debt_id}")
                return response["Item"]
            else:
                print(f"No debt found for debt_id: {debt_id}")
                return None

        except ClientError as e:
            print("An error occurred:", e)
            return None

    def add_user(self, user_data):
        print("-----------METODO AGREGAR USUARIO A LA BD-----------")
        try:
            if "id" in user_data:
                user_data["user_id"] = user_data.pop("id")

            user_data.setdefault("created_date", {"S": datetime.now().isoformat()})
            user_data.setdefault("projects", {"SS": []})
            user_data.setdefault("response_score", {"N": str(0)})

            dynamodb_client.put_item(TableName=self.users_table_name, Item=user_data)
            print(f"Usuario {user_data['user_id']['S']} agregado exitosamente")
        except ClientError as e:
            print(f"Ocurrió un error: {e}")

    def update_user(self, user_id, user_data):
        try:
            existing_user_data = self.get_user_data_from_db(user_id)
            self.add_new_data(existing_user_data, user_data)

            update_expression = "SET " + ", ".join(
                f"{k}=:{k}" for k in existing_user_data.keys() if k != "user_id"
            )
            expression_attribute_values = {
                f":{k}": v for k, v in existing_user_data.items() if k != "user_id"
            }

            dynamodb_client.update_item(
                TableName=self.users_table_name,
                Key={"user_id": {"S": user_id}},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
            )

            print(
                f"User data for {user_id} has been successfully updated in 'users' table."
            )
            for key, value in existing_user_data.items():
                print(f"{key}: {value}")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def get_all_debts_from_db(self):
        try:
            response = dynamodb_client.scan(TableName=self.table_name)
            items = response["Items"]
            return items
        except ClientError as e:
            print(f"Ocurrió un error: {e}")
            return None

    def add_new_data(self, existing_data, new_data):
        for key, value in new_data.items():
            if key not in existing_data:
                existing_data[key] = value
            elif isinstance(value, dict) and isinstance(existing_data[key], dict):
                self.add_new_data(existing_data[key], value)
            elif isinstance(value, list) and isinstance(existing_data[key], list):
                for item in value:
                    if item not in existing_data[key]:
                        existing_data[key].append(item)

    def get_user_data_from_db(self, user_id):
        try:
            response = dynamodb_client.get_item(
                TableName=self.users_table_name, Key={"user_id": {"S": user_id}}
            )
            item = response["Item"]
            return item
        except ClientError as e:
            print(f"Ocurrió un error: {e}")
            return None

    def get_debts_by_campaign_id(self, campaign_id: str):
        try:
            print(f"Scanning the Debts table for campaign_id: {campaign_id}")
            response = dynamodb_client.scan(
                TableName=self.table_name,
                FilterExpression="campaign_id = :campaign_id",
                ExpressionAttributeValues={":campaign_id": {"S": campaign_id}},
            )

            items = response["Items"]
            debts = [
                item
                for item in items
                if item.get("campaign_id", {}).get("S") == campaign_id
            ]

            if debts:
                print(f"Found {len(debts)} debts for campaign_id: {campaign_id}")
                return debts
            else:
                print(f"No debts found for campaign_id: {campaign_id}")
                return []

        except ClientError as e:
            print("An error occurred:", e)
            return None
