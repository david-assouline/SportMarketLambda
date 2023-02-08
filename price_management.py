import logging
import datetime
import dateutil.tz
import dateutil

from botocore.exceptions import ClientError

import toolkit
from constants.nhl_team_names import nhl_teams_list
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
nhl_table = client.Table('NHL')
nhl_historical_prices_table = client.Table('nhl_historical_prices')
user_historical_portfolio_table = client.Table('user_historical_portfolio_value')


def refresh_prices():
    response = {}
    total_outstanding_shares = toolkit.get_sum_outstanding_shares()
    for team in nhl_teams_list:
        outstanding_shares = toolkit.get_outstanding_shares_by_team_name(team)
        decimal_value = float(outstanding_shares) / float(total_outstanding_shares)
        new_price = decimal_value * 100
        set_share_price(team, str(round(float(new_price), 2)))
        response[team] = str(round(float(new_price), 2))
    print("Prices for all teams have been refreshed")
    return response


def set_share_price(team_name: str, value: str):
    try:
        response = nhl_table.update_item(
            Key={'team_name': team_name},
            UpdateExpression="SET #price = :update_value",
            ExpressionAttributeNames={
                "#price": "share_price"
            },
            ExpressionAttributeValues={
                ":update_value": value
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as err:
        logger.error("error")
        raise


def save_daily_closing_share_price():
    eastern = dateutil.tz.gettz('US/Eastern')
    today = datetime.datetime.now(tz=eastern).strftime('%d-%m-%Y')

    for i in nhl_teams_list:
        try:
            response = nhl_table.get_item(
                Key={'team_name': i},
            )
        except ClientError as err:
            logger.error("error")
            raise
        current_price = response["Item"]["share_price"]
        try:
            response = nhl_historical_prices_table.update_item(
                Key={'team_name': i},
                UpdateExpression="SET #date = :update_value",
                ExpressionAttributeNames={
                    "#date": today
                },
                ExpressionAttributeValues={
                    ":update_value": current_price
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as err:
            logger.error("error")
            raise


def save_end_of_day_portfolio_value():
    eastern = dateutil.tz.gettz('US/Eastern')
    today = datetime.datetime.now(tz=eastern).strftime('%d-%m-%Y')

    all_user_ids = toolkit.get_all_user_ids()

    for user_id in all_user_ids:
        try:
            response = user_historical_portfolio_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression="SET #date = :update_value",
                ExpressionAttributeNames={
                    "#date": today
                },
                ExpressionAttributeValues={
                    ":update_value": toolkit.get_total_value_of_user_portfolio(user_id)
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as err:
            logger.error("error")
            raise
