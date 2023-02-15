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
            "body": json.dumps(toolkit.get_user_balance(user_id))
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

    elif event['rawPath'] == "/register_user":
        new_user_id = event['queryStringParameters']['new_user_id']
        new_user_email = event['queryStringParameters']['new_user_email']

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(user_management.create_user(new_user_id, new_user_email))
        }
