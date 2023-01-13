import logging
from botocore.exceptions import ClientError

from dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')
nhl_table = client.Table('NHL')


def buy_shares(user_id: str, team_name: str, quantity: str):
    current_shares = get_portfolio_shares_by_team_name(user_id, team_name)
    try:
        if int(current_shares) > 0:
            response = users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression="SET #pf.#team = :update_value",
                ExpressionAttributeNames={
                    "#pf": "user_portfolio",
                    "#team": team_name
                },
                ExpressionAttributeValues={
                    ":update_value": str(int(quantity) + int(current_shares))
                },
                ReturnValues="UPDATED_NEW"
            )
            return f'Added {quantity} shares of {team_name} to portfolio of user #{user_id}' \
                   f'\nUser now has {int(quantity) + int(current_shares)} shares of {team_name}'
        else:
            users_table.put_item(
                Item={
                    "user_id": user_id,
                    "portfolio": {team_name: quantity}
                }
            )
    except ClientError as err:
        logger.error("error")
        raise


def get_portfolio_shares_by_team_name(user_id: str, team_name: str):
    try:
        response = users_table.get_item(
            Key={'user_id': user_id},
        )
    except ClientError as err:
        logger.error("error")
        raise
    else:
        portfolio = response["Item"]["user_portfolio"]
        try:
            return portfolio[team_name]
        except KeyError as e:
            return "0"


def get_outstanding_shares_by_team_name(team_name: str) -> str:
    try:
        response = nhl_table.get_item(
            Key={'team_name': team_name},
        )
    except ClientError as err:
        logger.error("error")
        raise
    else:
        value = response["Item"]["outstanding_shares"]
        print(f"There are {value} outstanding shares of {team_name}")
        return value

