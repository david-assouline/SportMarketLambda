import logging
from botocore.exceptions import ClientError

from constants.db_constants import USER_ID, USER_CASH_BALANCE, USER_PORTFOLIO, USER_EMAIL
from constants.nhl_team_names import *
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')


def create_user(user_id: str, user_email: str):

    item = {USER_ID: user_id, USER_EMAIL: user_email, USER_CASH_BALANCE: "10000", USER_PORTFOLIO: {MONTREAL_CANADIENS: '0',
                                                                                                CHICAGO_BLACKHAWKS: '0',
                                                                                                NEW_YORK_RANGERS: '0',
                                                                                                BOSTON_BRUINS: '0',
                                                                                                TORONTO_MAPLE_LEAFS: '0',
                                                                                                DETROIT_RED_WINGS: '0'
                                                                                                }}
    try:
        users_table.put_item(Item=item)
        print(f"Created user with ID {user_id} and cash balance 10000")
    except ClientError as err:
        logger.error("error")
        raise
