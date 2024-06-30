import uuid
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from .db_utils import dynamodb_resource


class DynamoDBPromiseService:
    def __init__(self):
        self.dynamodb = dynamodb_resource
        self.table_name = "payment_promises"
        self.payment_promise_table = self.dynamodb.Table(self.table_name)
        self.deserializer = TypeDeserializer()

    def deserialize_item(self, item):
        return {k: self.deserializer.deserialize(v) for k, v in item.items()}

    def create_payment_promise(
        self,
        project_id: str,
        campaign_id: str,
        assistant_id: str,
        call_id: str,
        user_id: str,
        amount: float,
        date: datetime,
    ):
        try:
            formatted_date = date.isoformat()
            promise_id = str(uuid.uuid4())
            current_date = datetime.now().isoformat()

            elements = {
                "promise_id": promise_id,
                "project_id": project_id,
                "campaign_id": campaign_id,
                "call_id": call_id,
                "current_date": current_date,
                "assistant_id": assistant_id,
                "user_id": user_id,
                "amount": Decimal(amount),
                "date": formatted_date,
            }
            response = self.payment_promise_table.put_item(Item=elements)
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 200:
                return True
            else:
                print(f"Error in put_item: HTTP Status Code {status_code}")
                return False

        except ClientError as e:
            print(
                f"ClientError creating payment promise: {e.response['Error']['Message']}"
            )
            return False
        except Exception as e:
            print(f"Error creating payment promise: {e}")
            return False
