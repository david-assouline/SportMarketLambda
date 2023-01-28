import uuid
import logging
from botocore.exceptions import ClientError

from constants.db_constants import USER_ID, USER_CASH_BALANCE, USER_PORTFOLIO
from constants.nhl_team_names import *
from resources.dynamodb import create_ddb_instance
from toolkit import get_user_balance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')


def create_user(starting_cash_balance: str):
    generated_guid = str(uuid.uuid1())
    item = {USER_ID: generated_guid, USER_CASH_BALANCE: starting_cash_balance, USER_PORTFOLIO: {MONTREAL_CANADIENS: '0',
                                                                                                CHICAGO_BLACKHAWKS: '0',
                                                                                                NEW_YORK_RANGERS: '0',
                                                                                                BOSTON_BRUINS: '0',
                                                                                                TORONTO_MAPLE_LEAFS: '0',
                                                                                                DETROIT_RED_WINGS: '0'
                                                                                                }}
    try:
        users_table.put_item(Item=item)
        print(f"Created user with ID {generated_guid} and cash balance {starting_cash_balance}")
    except ClientError as err:
        logger.error("error")
        raise
