import datetime
import logging
import dateutil.tz
import dateutil
from botocore.exceptions import ClientError

from constants.db_constants import USER_CASH_BALANCE, USER_PORTFOLIO, SHARE_PRICE, USER_NICKNAME, TRANSACTION_HISTORY
from constants.nhl_team_names import nhl_teams_list
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')
nhl_table = client.Table('NHL')
nhl_historical_prices_table = client.Table('nhl_historical_prices')


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


def get_user_portfolio(user_id: str):
    try:
        ddb_response = users_table.get_item(
            Key={'user_id': user_id},
        )
    except ClientError as err:
        logger.error("error")
        raise
    return {"user_portfolio": ddb_response["Item"][USER_PORTFOLIO],
            "transaction_history": ddb_response["Item"][TRANSACTION_HISTORY]}


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


def get_share_price_by_team_name(team_name: str):
    try:
        response = nhl_table.get_item(
            Key={'team_name': team_name},
        )
    except ClientError as err:
        logger.error("error")
        raise
    share_price = response["Item"][SHARE_PRICE]
    return share_price


def get_all_user_ids():
    response = users_table.scan(AttributesToGet=['user_id'])
    data = response['Items']
    all_user_ids = []
    for i in data:
        all_user_ids.append(i['user_id'])
    return all_user_ids


def get_total_value_of_user_portfolio(user_id: str):
    total_value = 0
    user_portfolio = get_user_portfolio(user_id)["user_portfolio"]
    for team_name in nhl_teams_list:
        total_value += float(user_portfolio[team_name]) * float(get_share_price_by_team_name(team_name))
    total_value = ('%.2f' % total_value)
    return str(total_value)


def get_previous_day_prices():
    values = {}
    eastern = dateutil.tz.gettz('US/Eastern')
    yesterday = (datetime.datetime.now(tz=eastern) - datetime.timedelta(days=1)).strftime('%d-%m-%Y')

    for team in nhl_teams_list:
        response = nhl_historical_prices_table.get_item(
            Key={'team_name': team},
        )
        share_price_yesterday = response["Item"][yesterday]
        values[team] = share_price_yesterday
    return values


def get_top_5_users():
    all_user_ids = get_all_user_ids()
    leaderboard_map = {}
    for user_id in all_user_ids:

        try:
            response = users_table.get_item(
                Key={'user_id': user_id},
            )
        except ClientError as err:
            logger.error("error")
            raise
        user_nickname = response["Item"][USER_NICKNAME]
        user_cash_balance = response["Item"][USER_CASH_BALANCE]
        user_portfolio_value = get_total_value_of_user_portfolio(user_id)
        total_assets = float(user_cash_balance) + float(user_portfolio_value)
        leaderboard_map[user_nickname] = str(total_assets)

    return leaderboard_map


def set_users_shares_by_team_name(user_id: str, team_name: str, value: str):
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
