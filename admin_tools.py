import logging

from botocore.exceptions import ClientError

from dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')


def set_shares(user_id: str, team_name: str, value: str):
    try:
        response = users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET #pf.#team = :update_value",
            ExpressionAttributeNames={
                "#pf": "user_portfolio",
                "#team": team_name
            },
            ExpressionAttributeValues={
                ":update_value": value
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Set {value} shares of {team_name} for user #{user_id}")
    except ClientError as err:
        logger.error("error")
        raise
