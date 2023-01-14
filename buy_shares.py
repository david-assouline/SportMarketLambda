import logging
from botocore.exceptions import ClientError

from dynamodb import create_ddb_instance

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')
nhl_table = client.Table('NHL')


#Main
def buy_shares(user_id: str, team_name: str, quantity: str):
    current_shares = get_portfolio_shares_by_team_name(user_id, team_name)
    purchase_cost = calculate_purchase_cost(team_name, quantity)
    if not user_has_sufficient_balance(user_id, purchase_cost):
        return "Insufficient funds for this transaction"
    try:
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
        deduct_shares_from_outstanding(team_name, quantity)
        charge_user(user_id, purchase_cost)

        return f'Added {quantity} shares of {team_name} to portfolio of user #{user_id}' \
               f'\nUser now has {int(quantity) + int(current_shares)} shares of {team_name}'
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


def deduct_shares_from_outstanding(team_name: str, quantity: str):
    current_outstanding = get_outstanding_shares_by_team_name(team_name)
    if (int(current_outstanding) - int(quantity)) < 0:
        raise ValueError("Not enough outstanding shares for this transaction")
    try:
        response = nhl_table.update_item(
            Key={'team_name': team_name},
            UpdateExpression="SET #outstanding = :update_value",
            ExpressionAttributeNames={
                "#outstanding": "outstanding_shares"
            },
            ExpressionAttributeValues={
                ":update_value": str(int(current_outstanding) - int(quantity))
            },
            ReturnValues="UPDATED_NEW"
        )
        print(
            f"Modified outstanding shares of {team_name} from {current_outstanding} to {str(int(current_outstanding) - int(quantity))}")
    except ClientError as err:
        logger.error("error")
        raise


def user_has_sufficient_balance(user_id: str, amount: str):
    try:
        response = users_table.get_item(
            Key={'user_id': user_id},
        )
    except ClientError as err:
        logger.error("error")
        raise
    value = response["Item"]["user_cash_balance"]
    if float(value) > float(amount):
        return True
    else:
        return False


def calculate_purchase_cost(team_name: str, amount_of_shares: str):
    try:
        response = nhl_table.get_item(
            Key={'team_name': team_name},
        )
    except ClientError as err:
        logger.error("error")
        raise
    share_price = response["Item"]["share_price"]
    purchase_cost = str(float(share_price) * float(amount_of_shares))
    print(f"Purchase cost of {amount_of_shares} shares of {team_name} costs {purchase_cost}")
    return purchase_cost


def charge_user(user_id: str, amount: str):
    user_balance = get_user_balance(user_id)
    try:
        response = users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET #balance = :update_value",
            ExpressionAttributeNames={
                "#balance": "user_cash_balance"
            },
            ExpressionAttributeValues={
                ":update_value": str(float(user_balance) - float(amount))
            },
            ReturnValues="UPDATED_NEW"
        )
        print(
            f"User {user_id} was charged {amount} and now has balance {str(float(user_balance) - float(amount))}")
    except ClientError as err:
        logger.error("error")
        raise


def get_user_balance(user_id: str):
    try:
        response = users_table.get_item(
            Key={'user_id': user_id},
        )
    except ClientError as err:
        logger.error("error")
        raise
    user_balance = response["Item"]["user_cash_balance"]
    print(f"User {user_id} has balance {user_balance}")
    return user_balance
