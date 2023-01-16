import buy_shares
import constants
import price_management
import user_management
from deposit import deposit_money
import toolkit

buy_shares.buy_shares("0bd6be7e-7d5d-4c60-a0e4-9f50f93b04c9",
                      constants.nhl_team_names.CHICAGO_BLACKHAWKS,
                      "74")
#toolkit.set_outstanding_shares_for_all("100")
#toolkit.get_sum_outstanding_shares()
#price_management.refresh_prices()
#user_management.create_user("5000")