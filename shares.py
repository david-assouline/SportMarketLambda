import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class Shares:
    def __init__(self, dyn_resource):
        self.table = dyn_resource

    def buy_shares(self, user_id: str, team_name: str, quantity: str):
        try:
            # self.table.put_item(
            #     Item={
            #         "user_id": user_id,
            #         "portfolio": {team_name: quantity}
            #     }
            # )
            response = self.table.update_item(
                Key={'user_id': '1'},
                UpdateExpression="SET #pf.#team = :update_value",
                ExpressionAttributeNames={
                    "#pf": "portfolio",
                    "#team": "Montreal Canadiens"
                },
                ExpressionAttributeValues={
                    ":update_value": "750"
                },
                ReturnValues="UPDATED_NEW"
            )

        except ClientError as err:
            logger.error(
                "Couldn't add movie %s to table %s. Here's why: %s: %s",
                team_name, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
