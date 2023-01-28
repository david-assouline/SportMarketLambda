import buy_shares
import constants
import price_management
import user_management
from deposit import deposit_money
import toolkit
import json


def lambda_handler(event, context):
    print(event)

    if event['rawPath'] == "/get_user_balance":
        user_id = event['queryStringParameters']['user_id']

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": f"User {user_id} has balance {toolkit.get_user_balance(user_id)}"
        }

    elif event['rawPath'] == "/get_prices":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(price_management.refresh_prices())
        }

    elif event['rawPath'] == "/get_user_portfolio":
        user_id = event['queryStringParameters']['user_id']

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(toolkit.get_user_portfolio(user_id))
        }
