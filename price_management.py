import logging
from botocore.exceptions import ClientError

import toolkit
from constants.nhl_team_names import nhl_teams_list
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
nhl_table = client.Table('NHL')


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
