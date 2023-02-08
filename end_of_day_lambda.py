import price_management


def lambda_handler(event, context):
    print(event)
    price_management.save_daily_closing_share_price()
    price_management.save_end_of_day_portfolio_value()
