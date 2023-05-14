import datetime
import dateutil.tz
import logging
from botocore.exceptions import ClientError

import price_management
import toolkit
from constants.db_constants import USER_CASH_BALANCE
from resources.dynamodb import create_ddb_instance
from toolkit import get_user_balance
from user_management import add_transaction_to_user_history

logger = logging.getLogger(__name__)

client = create_ddb_instance()
users_table = client.Table('Users')
nhl_table = client.Table('NHL')


def buy_shares(user_id: str, team_name: str, quantity: str):
    eastern = dateutil.tz.gettz('US/Eastern')
    date_today = datetime.datetime.now(tz=eastern).strftime('%d-%m-%Y %H:%M:%S')

    current_shares = get_portfolio_shares_by_team_name(user_id, team_name)
    purchase_cost = calculate_purchase_cost(team_name, quantity)
    if not user_has_sufficient_balance(user_id, purchase_cost):
        print("Insufficient funds for this transaction")
        return
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
        add_transaction_to_user_history(user_id, date_today, "buy", team_name, quantity, purchase_cost)
        add_shares_to_outstanding(team_name, quantity)
        charge_user(user_id, purchase_cost)
        price_management.refresh_prices()

        print(f'Added {quantity} shares of {team_name} to portfolio of user #{user_id}' \
              f'\nUser now has {int(quantity) + int(current_shares)} shares of {team_name}')
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


def add_shares_to_outstanding(team_name: str, quantity: str):
    current_outstanding = toolkit.get_outstanding_shares_by_team_name(team_name)
    try:
        response = nhl_table.update_item(
            Key={'team_name': team_name},
            UpdateExpression="SET #outstanding = :update_value",
            ExpressionAttributeNames={
                "#outstanding": "outstanding_shares"
            },
            ExpressionAttributeValues={
                ":update_value": str(int(current_outstanding) + int(quantity))
            },
            ReturnValues="UPDATED_NEW"
        )
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
    value = response["Item"][USER_CASH_BALANCE]
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
    print(f"Purchase cost of {amount_of_shares} shares of {team_name} is {purchase_cost}")
    return purchase_cost


def charge_user(user_id: str, amount: str):
    user_balance = get_user_balance(user_id)
    try:
        response = users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET #balance = :update_value",
            ExpressionAttributeNames={
                "#balance": USER_CASH_BALANCE
            },
            ExpressionAttributeValues={
                ":update_value": str(round(float(user_balance), 2) - round(float(amount), 2))
            },
            ReturnValues="UPDATED_NEW"
        )
        print(
            f"User {user_id} was charged {amount} and now has balance {str(float(user_balance) - float(amount))}")
    except ClientError as err:
        logger.error("error")
        raise
