import logging
from botocore.exceptions import ClientError

from constants.db_constants import USER_ID, USER_CASH_BALANCE, USER_PORTFOLIO, USER_EMAIL, USER_NICKNAME, \
    TRANSACTION_HISTORY
from constants.nhl_team_names import *
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')


def create_user(user_id: str, user_email: str, user_nickname: str):
    item = {USER_ID: user_id,
            USER_EMAIL: user_email,
            USER_NICKNAME: user_nickname,
            USER_CASH_BALANCE: "10000",
            USER_PORTFOLIO: {MONTREAL_CANADIENS: '0',
                             CHICAGO_BLACKHAWKS: '0',
                             NEW_YORK_RANGERS: '0',
                             BOSTON_BRUINS: '0',
                             TORONTO_MAPLE_LEAFS: '0',
                             DETROIT_RED_WINGS: '0'},
            TRANSACTION_HISTORY: {}
            }
    try:
        users_table.put_item(Item=item)
        print(f"Created user with ID {user_id} and cash balance 10000")
    except ClientError as err:
        logger.error("error")
        raise


def add_transaction_to_user_history(user_id: str, date: str, type: str, team_name: str, quantity: str, total: str):
    try:
        response = users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET #transaction_history.#date = :update_value",
            ExpressionAttributeNames={
                "#transaction_history": "transaction_history",
                "#date": date
            },
            ExpressionAttributeValues={
                ":update_value": {"transaction_type": type,
                                  "team_name": team_name,
                                  "transaction_quantity": quantity,
                                  "transaction_total": total}
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as err:
        logger.error("error")
        raise
