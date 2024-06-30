from .db_utils import dynamodb_client
from botocore.exceptions import ClientError


class DynamoDBCampaignService:
    def __init__(self):
        self.dynamodb_client = dynamodb_client
        self.table_name = "campaigns"

    def get_campaigns_by_project_id(self, project_id: str):
        try:
            response = self.dynamodb_client.query(
                TableName=self.table_name,
                IndexName="project_id-index",
                KeyConditionExpression="project_id=:project_id",
                ExpressionAttributeValues={":project_id": {"S": project_id}},
            )

            items = response["Items"]

            campaigns = [
                item
                for item in items
                if item["project_id"]["S"] == project_id
                and not item.get("is_deleted", {}).get("BOOL", False)
            ]

            if campaigns:
                return campaigns
            else:
                return []

        except ClientError as e:
            print("An error occurred: %s", e)
            return None
