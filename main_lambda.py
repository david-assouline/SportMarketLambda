import buy
import constants
import price_management
import sell
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

    elif event['rawPath'] == "/get_previous_day_prices":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(toolkit.get_previous_day_prices())
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
        new_user_nickname = new_user_email.split("@")[0]

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(user_management.create_user(new_user_id, new_user_email, new_user_nickname))
        }

    elif event['rawPath'] == "/buy":
        user_id = event['queryStringParameters']['user_id']
        team_name = event['queryStringParameters']['team_name']
        quantity = event['queryStringParameters']['quantity']

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(buy.buy_shares(user_id, team_name, quantity))
        }

    elif event['rawPath'] == "/sell":
        user_id = event['queryStringParameters']['user_id']
        team_name = event['queryStringParameters']['team_name']
        quantity = event['queryStringParameters']['quantity']

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(sell.sell_shares(user_id, team_name, quantity))
        }

    elif event['rawPath'] == "/leaderboard":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(toolkit.get_top_5_users())
        }
