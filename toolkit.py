import logging
from botocore.exceptions import ClientError

from constants.db_constants import USER_CASH_BALANCE
from constants.nhl_team_names import nhl_teams_list
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')
nhl_table = client.Table('NHL')


def get_user_balance(user_id: str):
    try:
        response = users_table.get_item(
            Key={'user_id': user_id},
        )
    except ClientError as err:
        logger.error("error")
        raise
    user_balance = response["Item"][USER_CASH_BALANCE]
    print(f"User {user_id} has balance {user_balance}")
    return user_balance


def get_sum_outstanding_shares() -> str:
    try:
        total_outstanding_shares = 0
        for team in nhl_teams_list:
            response = nhl_table.get_item(
                Key={'team_name': team},
            )
            total_outstanding_shares += int(response["Item"]["outstanding_shares"])
    except ClientError as err:
        logger.error("error")
        raise
    # print(f"The sum of outstanding shares is {total_outstanding_shares}")
    return str(total_outstanding_shares)


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
        return value


def set_shares_by_team_name(user_id: str, team_name: str, value: str):
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


def set_outstanding_shares_for_all(value: str):
    for team in nhl_teams_list:
        try:
            response = nhl_table.update_item(
                Key={'team_name': team},
                UpdateExpression="SET #outstanding = :update_value",
                ExpressionAttributeNames={
                    "#outstanding": "outstanding_shares"
                },
                ExpressionAttributeValues={
                    ":update_value": value
                },
                ReturnValues="UPDATED_NEW"
            )
            print(
                f"Set outstanding shares for {team} to {value}")
        except ClientError as err:
            logger.error("error")
            raise


def set_user_balance(user_id: str, value: str):
    try:
        response = users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET #balance = :update_value",
            ExpressionAttributeNames={
                "#balance": USER_CASH_BALANCE
            },
            ExpressionAttributeValues={
                ":update_value": value
            },
            ReturnValues="UPDATED_NEW"
        )
        print(
            f"Set user {user_id} balance to {value}")
    except ClientError as err:
        logger.error("error")
        raise