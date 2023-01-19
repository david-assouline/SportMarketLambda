import logging
from botocore.exceptions import ClientError

from constants.db_constants import USER_CASH_BALANCE
from resources.dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')


def deposit_money(user_id: str, amount: str):
    current_balance = get_user_current_balance(user_id)
    try:
        response = users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET #usercash = :update_value",
            ExpressionAttributeNames={
                "#usercash": USER_CASH_BALANCE
            },
            ExpressionAttributeValues={
                ":update_value": str(float(current_balance) + float(amount))
            },
            ReturnValues="UPDATED_NEW"
        )
        print(
            f"Deposited {amount} to user {user_id}. New balance: {str(float(current_balance) + float(amount))}")
    except ClientError as err:
        logger.error("error")
        raise


def get_user_current_balance(user_id: str):
    try:
        response = users_table.get_item(
            Key={'user_id': user_id},
        )
    except ClientError as err:
        logger.error("error")
        raise
    else:
        value = response["Item"][USER_CASH_BALANCE]
        print(f"User {user_id} has balance {value}")
        return value
